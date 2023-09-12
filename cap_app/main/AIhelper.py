from .RATCHET.model.transformer import Transformer, default_hparams
from .RATCHET.model.utils import create_target_masks
from tokenizers import ByteLevelBPETokenizer
import tensorflow as tf


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

    transformer.load_weights(
        'main\\Ratchet\\checkpoints\\RATCHET.tf').expect_partial()
    print(f'Model Loaded! Checkpoint file: checkpoints/RATCHET.tf')

    return transformer, tokenizer
