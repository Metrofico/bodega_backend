import re

from app_usbodega import utils


def validar_sesion_operacion(graphql_petition, *excepto):
    # print("OPERATION: ", graphql_petition["query"])
    query_r = str(graphql_petition["query"]).strip().replace("\n", "")
    query_r_spaces = re.sub("\s\s+", " ", query_r)
    query_str = query_r_spaces[query_r_spaces.find("{"):]
    spliter = query_str.lower().split(" ")
    tipo = spliter[0]
    if tipo == "query":
        query_obtenida = spliter[2]
        spliter_o = query_obtenida.split("(")
        operation = spliter_o[0]
    else:
        query_obtenida = spliter[1]
        spliter_o = query_obtenida.split("(")
        operation = spliter_o[0]
    # operation_name_recibido = graphql_petition["operationName"]
    print("Operacion: " + operation)
    print("Access: ", (operation in excepto[0]))
    if not (operation in excepto[0]):
        raise Exception("No autorizado")

    # print("EXCEPT: ", excepto)


def validar_sesion(contexto):
    try:
        cookies = getattr(contexto, 'cookies', None)
        if cookies is not None and "oAtmp" in cookies:
            token = cookies.get('oAtmp')
            decoded = utils.logindecode(token)
            if not decoded:
                raise Exception("No autorizado (Validator)")
    except (ValueError, Exception):
        raise Exception("No autorizado (Exception)")
