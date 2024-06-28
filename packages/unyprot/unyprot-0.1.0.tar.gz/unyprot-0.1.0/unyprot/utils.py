import re

def isValidID(string):
    if re.match("^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$", string):
        return True
    if re.match("^[A-Z]{3}[0-9]{5}$", string):
        return True    
    return False

def strip(string):
    subString = re.search(".xml$", string)
    if subString:
        return string.split(".")[0]

    return None