import datetime
import tensorflow as tf
import os
from main.singleton_manager import singleton_manager
from skimage import io
from tokenizers import ByteLevelBPETokenizer
import string
import random
from .models import Query
from .RATCHET.model.transformer import Transformer, default_hparams
from .RATCHET.model.utils import create_target_masks


def load_validator():

    validator_model = tf.keras.models.load_model(
        'main\\RATCHET\\checkpoints\\cxr_validator_model.tf')
    print('Validator Model Loaded!')
    return validator_model


def load_model():
    # Load Tokenizer
    tokenizer = ByteLevelBPETokenizer(
        'main\\RATCHET\\preprocessing\\mimic\\mimic-vocab.json',
        'main\\RATCHET\\preprocessing\\mimic\\mimic-merges.txt',
    )
    hparams = default_hparams()
    # Model Hyperparameters
    target_vocab_size = tokenizer.get_vocab_size()
    dropout_rate = 0.1
    num_layers = 6
    d_model = 512
    dff = 2048
    num_heads = 8

    transformer = Transformer(num_layers, d_model, num_heads, dff,
                              target_vocab_size=target_vocab_size,
                              dropout_rate=dropout_rate)
    print(os.getcwd() + "here")
    file_path = os.path.join('main', 'RATCHET', 'checkpoints', 'RATCHET.tf')
    transformer.load_weights(file_path).expect_partial()
    print(f'Model Loaded! Checkpoint file: checkpoints/RATCHET.tf')
    return transformer, tokenizer


def top_k_logits(logits, k):
    if k == 0:
        # no truncation
        return logits

    def _top_k():
        values, _ = tf.nn.top_k(logits, k=k)
        min_values = values[:, -1, tf.newaxis]
        return tf.where(
            logits < min_values,
            tf.ones_like(logits, dtype=logits.dtype) * -1e10,
            logits,
        )
    return tf.cond(
        tf.equal(k, 0),
        lambda: logits,
        lambda: _top_k(),
    )


def top_p_logits(logits, p):
    """Nucleus sampling"""
    batch, _ = logits.shape.as_list()
    sorted_logits = tf.sort(logits, direction='DESCENDING', axis=-1)
    cumulative_probs = tf.cumsum(
        tf.nn.softmax(sorted_logits, axis=-1), axis=-1)
    indices = tf.stack([
        tf.range(0, batch),
        # number of indices to include
        tf.maximum(tf.reduce_sum(
            tf.cast(cumulative_probs <= p, tf.int32), axis=-1) - 1, 0),
    ], axis=-1)
    min_values = tf.gather_nd(sorted_logits, indices)
    return tf.where(
        logits < min_values,
        tf.ones_like(logits) * -1e10,
        logits,
    )


def evaluate(inp_img, tokenizer, transformer, temperature, top_k, top_p, options, seed, comment, interactive=False, MAX_LENGTH=128):

    # The first token to the transformer should be the start token
    output = tf.convert_to_tensor([[tokenizer.token_to_id('<s>')]])

    if interactive:
        inp_text = comment
        if inp_text != '':
            input_text = tf.convert_to_tensor([tokenizer.encode(inp_text).ids])
            output = tf.concat([output, input_text], axis=-1)

    last_entry = Query.objects.order_by('-id').first()

    for i in range(MAX_LENGTH):
        # Remove the last token ("<s>") to continue the context
        if interactive:
            current_report = tokenizer.decode(tf.squeeze(output, axis=0)[1:])
            print(f'Current report: {current_report}')

            # let user add more text
            adapted_report = current_report
            if adapted_report != '':
                if adapted_report == 'exit':
                    interactive = False
                else:
                    adapted_report = tf.convert_to_tensor(
                        [tokenizer.encode(adapted_report).ids])
                    output = tf.convert_to_tensor(
                        [[tokenizer.token_to_id('<s>')]])
                    output = tf.concat([output, adapted_report], axis=-1)

        combined_mask = create_target_masks(output)
        predictions = transformer([inp_img, output], training=False)
        predictions = predictions[:, -1, :] / temperature
        predictions = top_k_logits(predictions, k=top_k)
        predictions = top_p_logits(predictions, p=top_p)

        if options == 'Greedy':
            predicted_id = tf.cast(
                tf.argmax(predictions, axis=-1), tf.int32)[:, tf.newaxis]
        elif options == 'Sampling':
            predicted_id = tf.random.categorical(
                predictions, num_samples=1, dtype=tf.int32, seed=seed)
        else:
            print('SHOULD NOT HAPPEN')

        if predicted_id == 2:
            return tf.squeeze(output, axis=0)[1:], transformer.decoder.last_attn_scores

        output = tf.concat([output, predicted_id], axis=-1)

    return tf.squeeze(output, axis=0)[1:], transformer.decoder.last_attn_scores


def randomString():
    S = 20  # number of characters in the string.
# call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
# print("The randomly generated string is : " + str(ran)) # print the random data
    return str(ran)


def AIReport(image, url, comment):
  #  report = "This is a report for image: "+image+"\n" +"at "+ url+"\n" +"and comment: "+comment
   # transformer, tokenizer = load_model()
    transformer = singleton_manager.get_transformer()
    tokenizer = singleton_manager.get_tokenizer()
    cxr_validator_model = singleton_manager.get_cxr_validator_model()
    print(os.path.exists("main\RATCHET\checkpoints\RATCHET.tf"))

    options = 'Greedy'
    seed = 42
    temperature = 1.0
    top_k = 6
    top_p = 1.0
    attention_head = -1
    last_entry = Query.objects.order_by('-id').first()
    interactive = True
    comment2 = comment
    uploaded_file = last_entry.image
    if uploaded_file:

        # Read input image with size [1, H, W, 1] and range (0, 255)
        img_array = io.imread(uploaded_file, as_gray=True)[None, ..., None]

        # Convert image to float values in (0, 1)
        img_array = tf.image.convert_image_dtype(img_array, tf.float32)

        # Resize image with padding to [1, 224, 224, 1]
        img_array = tf.image.resize_with_pad(
            img_array, 224, 224, method=tf.image.ResizeMethod.BILINEAR)

        # Check image
        valid = tf.nn.sigmoid(cxr_validator_model(img_array))
        if valid < 0.1:
            print('Image is not a Chest X-ray')
            return

        # Log datetime
        print('[{}] Running Analysis...'
              .format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Generate radiology report

        result, attention_weights = evaluate(img_array, tokenizer, transformer,
                                             temperature, top_k, top_p,
                                             options, seed, comment2, interactive, 128)

        predicted_sentence = tokenizer.decode(result)

    return predicted_sentence
