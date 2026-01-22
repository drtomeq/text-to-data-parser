'''
Introduction
    take data in text format and make a data structure based on it
    can make dictionaries, lists and sets
    also allows for multiple layers of nesting of different data structures

Application
    orignally made to make a structure for input data in tkinter
    designed for several data inputs in multiple frames 
    but can be used more generally for text files
    or text from another program

Formatting 
  assume data follows certain formatting rules, e.g.
    data on each line is a separate element of a list
    sets and dictionaries have "{" and lists "[" as their first character
        These characters should only be used to start a data structure
        some characters are stripped from the start , e.g. spaces and quotations 
        this might help detect structures that don't start in the first character
    closure of each list etc is done in the opposite order to which they are opened
    each item is separated/ delimited by a comma
    leading and final spaces and quotation marks are ignored for each data point
    Unlike standard Python, nesting in sets is allowed
        In this case a dictionary is produced
        the values are those in the set
        the keys have the word "set" and increment the number  

Issues and Future Work
  Potential limitations/ problems that may be addressed in a future version include:
    content in quotation marks are not automatically treated as strings 
    tuples, or generally data in round barackets, are not considered
    it is functional for my use, but could be made more efficient
    error checking and exceptions
'''

def get_file_lines(filer = "my_data.txt"):
    with open(filer, "r") as file:
        file_data = file.readlines()
        return file_data

def get_type(str_in):
    charr = str_in[0]
    if charr == "{":
        if ":" in str_in:
            return dict
        return set
    if charr == "[":
        return list
    return str

def nesting_levels(my_text):
    levels = []
    current_level = 0
    for charr in my_text:
        if charr in ["[", "{"]:
            current_level += 1
        elif charr in ["]", "}"]:
            current_level -=1
        levels.append(current_level)
    return levels

def remove_left_chars(str_in):
    unwanted = [" ", "\"", "'", "\""]
    pos = 0
    while str_in[pos] in unwanted:
        pos +=1
    return str_in[pos:]

def remove_right_chars(str_in):
    unwanted = [" ", "\"", "'", "\"", "}", "]"]
    pos = -1
    while str_in[pos] in unwanted:
        pos -=1
    return str_in[:pos+1]


def make_list(my_text, levels):    
    # assume that data structures begin and end with a character 
    # indicating the type e.g. { for begin dictionary 
    # or else it is a string
    typer = get_type(my_text)

    if typer == str:
        return (typer, my_text)

    my_list = []
    entry = ""
    # current_pos = 1 # not 0 as that will the [ character
    for pos in range(1,len(my_text)):
        if my_text[pos]  == "," and levels[pos] == 1:
            my_list.append(entry)
            entry = ""
        else:
            entry += str(my_text[pos])
    # the final entry to add, everything after the last comma
    my_list.append(entry)
    return typer, my_list

def convert_to_dict(listy):
    # each entry of the list should include both the key and the value
    # up to the collon should be the key
    # everything after should be the value
    dicter = {}

    for element in listy:
        pos = 0
        for charr in element:
            if charr == ":":
                break
            pos += 1
        # +1 to exclude the colon
        value = element[pos+1:]
        keyer = element[:pos]
        keyer = remove_right_chars(remove_left_chars(keyer))
        dicter[keyer] = value
    return dicter

def inner_dict(dict_in):
    # assume the keys are already good
    # but check for inner structure of the values
    new_dict = {}
    for keyer in dict_in:
        new_dict[keyer] = inner_lists(dict_in[keyer])
    return new_dict

def set_convert(list_in):
    # if there is no nesting, do a straight conversion to a set
    # ignore first char which is the list symbol
    strr = str(list_in)
    if "[" not in strr[1:] and "{" not in strr[1:]:
        return set(list_in)

    # you can't have nested lists in sets but can in dictionaries
    # nor can dictionary keys be lists
    # so will convert the set into values of a dictionary
    # for the keys use "set" and a number so you know it was originally a set
    dicter = {}
    for num,val in enumerate(list_in):
        dicter["set"+str(num)] = val
    return dicter

# will look for any type of inner data structure, not just lists
#  and then those nested in this one
# the name is a legacy of an older version
def inner_lists(my_text):
    my_text = remove_left_chars(my_text)
    levs = nesting_levels(my_text)
    typer, listy = make_list(my_text, levs)
    if  typer==str:
        return remove_right_chars(listy)
    #if type(listy) == list:
    if typer == list:
        for i in range(len(listy)):
            listy[i] = inner_lists(listy[i])
    elif type(listy) == set:
        print("already converted to set")
        for item in listy:
            inner = inner_lists(item)
            listy.remove(item)
            listy.add(inner)
    elif typer == set:     
        print("set")   
        # this is when it is still a list and hasn't been converted to a set
        listy = set_convert(listy)
        # if there is no nesting, it stays as a set and return as is
        if type(listy) == set:
            return listy
        # otherwise it should be converted into a dictionary
        typer = dict
    elif type(listy) == dict:
        listy = inner_dict(listy)
    elif typer == dict:
        listy = convert_to_dict(listy)
        listy = inner_dict(listy)
    return listy
        
lines = get_file_lines()
datar = []
for liner in lines:
    datar.append(inner_lists(liner))
print(datar)
