import json
from django.http import HttpResponse
from django.shortcuts import render

from main.AIcode import *
from django.http import JsonResponse
from .forms import QueryForm
from .models import Query
from .serializers import QuerySerializer
from django.core import serializers
from main.singleton_manager import singleton_manager



def index(request):
    return render(request, 'index.html')


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
    else:
        form = QueryForm()
    return render(request, 'index.html', {'form': form})


def generate(request):
    AIoutput = ""  # Set a default value for the variable

    # if(request.GET.get('mybtn=Generate')):
    last_entry = Query.objects.order_by('-id').first()
    if last_entry:
        AIinput = last_entry.inputText

        # Split AIinput into comments using '@@' as the delimiter
        comments = AIinput.split('@@')

        if comments:
            # Extract the last comment
            last_comment = comments[-1]

            # Generate AI output based on the last comment
            AIoutput = AIReport(
                last_entry.title, last_entry.image.name, last_comment)

            # Update the outputText with the full AIoutput
            if last_entry.outputText:
            # Append the new comment to the existing content with @@
                last_entry.outputText = f"{last_entry.outputText}@@{AIoutput}"
            else:
            # Set the inputText directly if it's empty
           
                last_entry.outputText = AIoutput

            # Increment the clicks
            last_entry.clicks += 1
            last_entry.save()
        else:
            # No '@@' separators found, use AIinput directly as the comment
            AIoutput = AIReport(
                last_entry.title, last_entry.image.name, AIinput)

    return JsonResponse({"AIoutput": AIoutput})


def load_model(request):
    transformer = singleton_manager.get_transformer()
    tokenizer = singleton_manager.get_tokenizer()
    cxr_validator_model = singleton_manager.get_cxr_validator_model()
    return JsonResponse({"status": "success"})


def stats(request):
    # if request.method == 'GET':
    last_entry = Query.objects.order_by('-id').first()
    difference = []
    report = ""
    arr1,arr2 = split_strings_by_delimiter(last_entry.inputText, last_entry.outputText)
    differences = compare_all_strings_in_array(arr2, arr1)
    #call compare_strings in a loop to compare all the strings in the array
    for difference in differences:
        print(difference) 
    if last_entry:
        serialized_data = serializers.serialize('json', [last_entry])
        #python code to append the differences to the serialized data
        report=split_string_by_delimiter_and_get_last(last_entry.outputText)
        response_data = {
        
            
            'title': last_entry.title,
            'image': last_entry.image.name,
            'inputText': last_entry.inputText,
            'outputText': report,
            'clicks': last_entry.clicks,
            'createdAt': last_entry.createdAt,
        
            # Add other fields from last_entry here
        
        'userInput': differences
    }

    # Serialize the dictionary to JSON
        #json_response = json.dumps(response_data)
       # additional_data = {'last_entry': serialized_data, 'userInput': difference}
        print(response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({'message': 'No data available.'})


def comment(request):
    # Get the input_text data from the POST request
    input_text = request.POST.get("input_text", " ")
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['input_text']
    print(content)
    # Save the input_text to the database
    last_entry = Query.objects.order_by('-id').first()
    if last_entry:
        if last_entry.inputText:
            # Append the new comment to the existing content with @@
            last_entry.inputText = f"{last_entry.inputText}@@{content}"
        else:
            # Set the inputText directly if it's empty
            last_entry.inputText = content

        last_entry.save()  # Save the changes to the database
        print(last_entry.inputText)
        return JsonResponse({'status': 'success'})
    else:
        # Return an error response as a JSON if no entry is found in the database
        return JsonResponse({'status': 'error', 'message': 'No entry found in the database.'})

#python code to split strings by delimiter @@ and return two arrays
def split_strings_by_delimiter(input, output):
    arr1 = input.split("@@")
    arr2 = output.split("@@")
    return arr1,arr2
def split_string_by_delimiter_and_get_last(input_string):
    parts = input_string.split("@@")
    if len(parts) > 0:
        return parts[-1]
    else:
        # Return an empty string if there are no parts after splitting
        return ""

#python code to compare two arrays of strings and return the differences   
def compare_arrays_of_strings(arr1, arr2):
    differences = []
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            differences.append(i)
    return differences  
#python code to compare two strings and return the different characters
def compare_strings(str1, str2):
    differences = []
    # Find the common prefix between the two strings
    common_prefix = ''
    for char1, char2 in zip(str1, str2):
        if char1 == char2:
            common_prefix += char1
        else:
            break

    # Extract the differing part of the second string
    differing_part = str2[len(common_prefix):]

    # Check if the differing part is not empty
    if differing_part.strip():
        differences.append(differing_part.strip())
    return differences

def compare_all_strings_in_array(string_array1, string_array2):
    differences_array = []

    for i in range(len(string_array1)):
        words1 = string_array1[i].split()
        words2 = string_array2[i].split()
        
        differences = [word for word in words2 if word not in words1]
        
        if differences:
            differences_array.append(' '.join(differences))
            

    return differences_array
def concatenate_strings(string_array):
   
    return " ".join(string_array)