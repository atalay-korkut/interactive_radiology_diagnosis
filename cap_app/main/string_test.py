
input = "In comparison with the study of ___, there is little overall change. \
Again there is a small right apical pneumothorax.  The right lung is essentially \
clear.  The right IJ catheter has been removed. Right pleural opacity@@In comparison with the study of ___, there is little overall change. \
Again there is a small right apical pneumothorax.  The right lung is essentially \
clear.  The right IJ catheter has been removed. Right pleural opacity is \
again seen.@@In comparison with the study of ___, there is little overall change. \
Again there is a small right apical pneumothorax.  The right lung is essentially \
clear.  The right IJ catheter has been removed. Right pleural opacity is \
again seen. Chest wall compatible with@@In comparison with the study of ___, there is little overall change. \
Again there is a small right apical pneumothorax.  The right lung is essentially \
clear.  The right IJ catheter has been removed. Right pleural opacity is \
again seen. Chest wall compatible with the known mass."

output="In comparison with the study of ___, there is little overall change. \
Again there is a small right apical pneumothorax. The right lung is essentially \
clear. The right IJ catheter has been removed.@@In comparison with the study of ___, there is little overall change. \
Again there is a small right apical pneumothorax. The right lung is essentially \
clear. The right IJ catheter has been removed. Right pleural opacity is \
again seen.@@In comparison with the study of ___, there is little overall change. \
Again there is a small right apical pneumothorax. The right lung is essentially \
clear. The right IJ catheter has been removed. Right pleural opacity is \
again seen.@@In comparison with the study of ___, there is little overall change. \
Again there is a small right apical pneumothorax. The right lung is essentially \
clear. The right IJ catheter has been removed. Right pleural opacity is \
again seen. Chest wall compatible with the known mass."

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
    """
    Concatenate an array of strings into a single string, separated by a delimiter.

    Args:
    string_array (list): The array of strings to concatenate.
    delimiter (str, optional): The delimiter to use between each string. Default is a space.

    Returns:
    str: The concatenated string.
    """
    return " ".join(string_array)

def main():
    print("Hello World!")
    arr1,arr2 = split_strings_by_delimiter(input, output)
    differences = compare_all_strings_in_array(arr2, arr1)
    #call compare_strings in a loop to compare all the strings in the array
    print(concatenate_strings(differences))
    
   
         

if __name__ == "__main__":
    main()   