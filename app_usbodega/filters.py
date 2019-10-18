def max_length(string, maxlenght, errormessage):
    if not (len(string) <= maxlenght):
        errormessage = str(errormessage).replace("$length", str(maxlenght))
        raise Exception(errormessage)
    pass


def strfilters(**kwargs):
    if "max_length" in kwargs:
        max_length(kwargs.get("str"), kwargs.get("max_length"), kwargs.get("errormessagemaxlength"))
    if "min_length" in kwargs:
        min_length(kwargs.get("str"), kwargs.get("min_length"), kwargs.get("errormessageminlength"))


def min_length(string, minlenght, errormessage):
    if not (len(string) >= minlenght):
        errormessage = str(errormessage).replace("$length", str(minlenght))
        raise Exception(errormessage)
    pass
