# text-to-data-parser

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
