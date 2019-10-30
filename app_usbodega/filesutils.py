def allowextension(ext, *args):
    isallowed = False
    allowed = None
    for arg in args:
        if ext == arg:
            isallowed = True
            break
    if not isallowed:
        allowed = str(args).replace("(", "").replace(")", "").rstrip(",")
    return "El archivo no es soportado, debe ser almenos de extensión: " + allowed if not (allowed is None) else None
