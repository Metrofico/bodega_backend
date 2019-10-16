def max_length(string, maxlenght):
    if not (len(string) <= maxlenght):
        raise Exception("El máximo de caracteres es " + str(maxlenght))
    pass


def strfilters(**kwargs):
    if "max_length" in kwargs:
        max_length(kwargs.get("str"), kwargs.get("max_length"))
    if "min_length" in kwargs:
        min_length(kwargs.get("str"), kwargs.get("min_length"))


def min_length(string, minlenght):
    if not (len(string) >= minlenght):
        raise Exception('El mínimo de caracteres es ' + str(minlenght))
    pass
