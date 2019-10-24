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


def verificar(nro):
    l = len(nro)
    if l == 10 or l == 13:  # verificar la longitud correcta
        cp = int(nro[0:2])
        if 1 <= cp <= 22:  # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if 0 <= tercer_dig < 6:  # numeros enter 0 y 6
                if l == 10:
                    return __validar_ced_ruc(nro, 0)
                elif l == 13:
                    return __validar_ced_ruc(nro, 0) and nro[
                                                         10:13] != '000'  # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                return __validar_ced_ruc(nro, 1)  # sociedades publicas
            elif tercer_dig == 9:  # si es ruc
                return __validar_ced_ruc(nro, 2)  # sociedades privadas
    return False


def __validar_ced_ruc(nro, tipo):
    total = 0
    if tipo == 0:  # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])  # digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1:  # r.u.c. publicos
        base = 11
        d_ver = int(nro[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2)
    elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(nro[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    for i in range(0, len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
        else:
            total += p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver


def has_value(value, term):
    if value != "":
        return True
    else:
        raise Exception("¡El campo " + term + " esta vacio!")


def get_tipo_documento(tipo_doc):
    if tipo_doc > 2 or tipo_doc == 0:
        raise Exception("Tipo de documento invalido, indices validos: 1 (Cédula), 2 (Pasaporte)")
    else:
        return "Cédula" if tipo_doc == 1 else "Pasaporte"


def exists_field(model, field, dato, upper_case):
    if upper_case:
        dato = str.upper(dato)
    data = model.objects.filter(**{field: dato})
    return data.count() != 0