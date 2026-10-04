# Mock louis module to bypass liblouis dependency
def translateString(table, text, mode=None):
    """Mock translation function that returns the input text unchanged"""
    return text

def backTranslateString(table, text, mode=None):
    """Mock back translation function that returns the input text unchanged"""
    return text

# Mock constants
noContractions = 1
noUndefined = 2
