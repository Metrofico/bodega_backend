def allowextension(ext, *args):
    isallowed = False
    for arg in args:
        if ext == arg:
            isallowed = True
            break
    if not isallowed:
        raise Exception("El archivo soportado debe ser: ", str(args))
    return isallowed
