import json
import math
import re
import time
from datetime import datetime

import graphene
from django.conf import settings
from django.core.management.color import no_style
from django.db import connection
from graphene_file_upload.scalars import Upload

import manage
from app_usbodega.sockets import tcpclient
from app_usbodega import filesutils, utils
from app_usbodega.graphql.objetos.ObjectsTypes import CatalogoType, CatalogoUpdateCurrent
from app_usbodega.graphql.subscription.CatalogoSubscription import CatalogoSuscription
from app_usbodega.graphql.subscription.NotificacionesSubscription import NotificacionesSubscription
from app_usbodega.graphql.subscription.PersonalNotificacionesSubscription import PersonalNotificacionesSubscription
from app_usbodega.models import Catalogos, CurrentCatalogo
from tabula_py import tabula

ID_DE_EXISTENCIA = "ID EXISTENCIA"
DESCRIPCION = "DESCRIPCION"
TABULA_SERVER = False


def redondear(n):
    if n == 0:
        return 0
    sgn = -1 if n < 0 else 1
    scale = int(-math.floor(math.log10(abs(n))))
    if scale <= 0:
        scale = 1
    factor = 10 ** scale
    return sgn * math.floor(abs(n) * factor) / factor


class LastCatalogo(graphene.AbstractType):
    lastcatalogo = graphene.Field(CatalogoType)
    updatecurrentcatalogo = graphene.Field(CatalogoUpdateCurrent, catalogo=graphene.String(required=True))

    def resolve_lastcatalogo(self, info):
        if Catalogos.objects.all().count() == 0:
            raise Exception("No hay datos para mostrar")
        catalogo = Catalogos.objects.last()
        csvpath = catalogo.file
        csvpath = csvpath.replace("{BODEGA_FOLDER}", settings.BODEGA_FOLDER)
        csvpath = csvpath.replace("{DB_FILES_STATIC}", settings.DB_FILES_STATIC)
        input_file = open("." + csvpath, "r")
        csvcontent = input_file.read()
        return CatalogoType(payload=csvcontent)

    def resolve_updatecurrentcatalogo(self, info, catalogo):
        if Catalogos.objects.all().count() == 0:
            raise Exception("No hay datos para procesar en el catálogo")
        try:
            catalogo_object = Catalogos.objects.get(nameFile=catalogo + ".pdf")
        except Exception:
            raise Exception("No existe un catálogo con ese nombre")
        csvpath = catalogo_object.file
        csvpath = csvpath.replace("{BODEGA_FOLDER}", settings.BODEGA_FOLDER)
        csvpath = csvpath.replace("{DB_FILES_STATIC}", settings.DB_FILES_STATIC)
        print(csvpath)
        input_file = open("." + csvpath, "r")
        csvcontent = input_file.read()
        processjson(csvcontent)
        return CatalogoUpdateCurrent(
            success="El cátalogo ha sido procesado correctamente, ya esta disponible para mostrarse")


def replace_last_word(text, word):
    spliter = str(text).split(" ")
    index = len(spliter)  # empieza con 1
    lastword = str(spliter[len(spliter) - 1]).replace(word, "")
    text = spliter[:index - 1]
    textappend = ""
    for word in text:
        textappend = textappend + " " + str(word)
    textappend = textappend + " " + lastword
    textappend = str(textappend).strip()
    return textappend


def replace_last_two_words(text):
    words = ["UNIDAD", "N"]
    spliter = str(text).split(" ")
    index = len(spliter)  # empieza con 1
    if index > 1:
        antepenultima = str(spliter[len(spliter) - 2])
        lastword = str(spliter[len(spliter) - 1])
        if antepenultima == words[0]:
            antepenultima = antepenultima.replace(words[0], "")
            lastword = lastword.replace(words[1], "")
        text = spliter[:index - 2]
        textappend = ""
        for word in text:
            textappend = textappend + " " + str(word)
        textappend = textappend + " " + antepenultima + " " + lastword
        textappend = str(textappend).strip()
    else:
        textappend = text
    return textappend


def extract_code_from_description(text):
    spliter = str(text).split(" ")
    index = len(spliter)  # empieza con 1
    lastword = str(spliter[len(spliter) - 1])
    lastword_extract_id = None
    if "-" in lastword:
        spliter_lastword = str(lastword).split("-")
        code = spliter_lastword[1]
        if len(code) is 6:
            code0 = spliter_lastword[0]
            count = 0
            count_before = 0
            for cha in code0:
                try:
                    int(cha)
                    count = count + 1
                except ValueError:
                    pass
            code0before = code0[1::2]
            correct_word = code0[::2]
            for cha_before in code0before:
                try:
                    int(cha_before)
                    count_before = count_before + 1
                except ValueError:
                    pass
            if count is 6 and count_before is 6:
                lastword_extract_id = str(code0before) + "-" + str(code)
                lastword = str(lastword).replace(str(lastword), str(correct_word))
    text = spliter[:index - 1]
    textappend = ""
    for word in text:
        textappend = textappend + " " + str(word)
    textappend = textappend + " " + lastword
    textappend = str(textappend).strip()
    return {"code": lastword_extract_id, "newtext": textappend}


def processjson(jsoncontent):
    CatalogoSuscription.catalogo_status(0, 0, 0, "CARGANDO DATOS DE CATÁLOGO")
    reset_sql_current_catalogo()
    datas = json.loads(jsoncontent)
    CatalogoSuscription.catalogo_status(0, 0, 0, "CÁLCULANDO TIEMPO RESTANTE")
    start = time.time()
    count = 0
    total = len(datas)
    controler_interval = 100
    controler_count = 0
    elapsed = -1
    NotificacionesSubscription.enviar_notificacion("warning", "Sé ha empezado a reemplazar el cátalogo actual")
    for element in datas:
        if controler_count == controler_interval:
            controler_count = 0
            end = time.time()
            elapsed = end - start
        id_existencia = str(element["ID EXISTENCIA"])
        descripcion = str(element["Unnamed: 1"])
        item_presu = str(element["LOTE"])
        umedida = str(element["U. MEDIDA"])
        caducidad = str(element["CADUCIDAD"])
        if item_presu is "N":
            item_presu = str(element["ITEM PRESUPUESTARIO"])
        if "-" in umedida:
            item_presu = str(umedida)
        if "-" in caducidad:
            item_presu = caducidad
        re.sub("\s\s+", " ", descripcion)
        id_existencia = id_existencia if len(id_existencia) >= 16 else "0" + id_existencia
        dic_descripcion = extract_code_from_description(descripcion)
        if not dic_descripcion["code"] is None:
            item_presu = dic_descripcion["code"]
            descripcion = dic_descripcion["newtext"]
        descripcion = replace_last_word(descripcion, "UNIDAD")
        descripcion = replace_last_two_words(descripcion)
        current_catalogo = CurrentCatalogo(id_de_existencia=id_existencia, descripcion=descripcion,
                                           item_presupuestario=item_presu)
        current_catalogo.save()
        if controler_count == 20:
            if elapsed != -1:
                remaing_timing = (((total - count) * elapsed) / count)
                CatalogoSuscription.catalogo_status(count, total, utils.segundos_a_formato(remaing_timing), "running")
        count = count + 1
        controler_count = controler_count + 1
    CatalogoSuscription.catalogo_status(0, 0, 0, "")
    NotificacionesSubscription.enviar_notificacion("success", "Se ha actualizado el cátalogo")
    print("Cátalogo ha sido procesado correctamente")
    pass


def tarea_completada_de_conversion(success, user_id):
    global TABULA_SERVER
    TABULA_SERVER = False
    if success:
        print("La tarea terminó")
    else:
        print("La taréa no terminó con exito")
    pass


class Catalogo(graphene.Mutation):
    class Arguments:
        file = Upload()

    success = graphene.Boolean()

    def mutate(self, info, file=None):
        global TABULA_SERVER
        if TABULA_SERVER:
            raise Exception("Hay un cátalogo en proceso de conversión, por favor espere")
        TABULA_SERVER = True
        auth_user = getattr(info.context, "auth", None)
        user_id = auth_user.get("id")
        if file is not None:
            name = file.name
            namesplit = str(name).split(".")
            ext = ""
            if len(namesplit) > 1 and str(namesplit[len(namesplit) - 1]).strip():
                index = len(namesplit)
                ext = namesplit[index - 1]
            if not str(namesplit[0]).strip():
                name = name
            else:
                name = namesplit[0]
            now = datetime.now()
            date = datetime.timestamp(now)
            namepdf = name + str(date) + ".pdf"
            namejson = name + str(date) + ".json"
            print("Nombre de archivo: ", namepdf)
            extensionallow = filesutils.allowextension(ext, "pdf")
            if not (extensionallow is None):
                TABULA_SERVER = False
                raise Exception(extensionallow)
            print("Iniciando conversion a json!: ", namejson)
            PersonalNotificacionesSubscription.enviar_notificacion(user_id, "success",
                                                                   "El archivo fue subido con éxito, y se está "
                                                                   "procesando su solicitud de conversión por favor "
                                                                   "espere")
            dbfiles_out_converted = "./" + settings.DB_FILES_STATIC + "/" + settings.BODEGA_FOLDER + "/" + namejson
            dbfiles_out_pdf = "./" + settings.DB_FILES_STATIC + "/" + settings.BODEGA_FOLDER + "/" + namepdf
            dbfiles_out_replazable = "./" + "{DB_FILES_STATIC}" + "/{BODEGA_FOLDER}/" + namejson
            bytess = file.read()
            out_file = open(dbfiles_out_pdf, "wb")  # archivo [w]rite(escribir) como [b]inary(binario)
            out_file.write(bytess)
            out_file.close()

            leer_archivo_ruta = manage.db_bodega_file_path(namepdf)
            archivo_salida = manage.db_bodega_file_path(namejson)
            initial_convertion = f"-convert --pages all --guess --format JSON --outfile {archivo_salida} --silent " \
                                 f"{leer_archivo_ruta}\n"
            tcpclient.ClientTCP(settings.TABULA_SERVER_HOST, settings.TABULA_SERVER_PORT,
                                initial_convertion, user_id, namepdf, dbfiles_out_replazable, date,
                                callback=tarea_completada_de_conversion).start()
            success = True
            return Catalogo(success=success)


def reset_sql_current_catalogo():
    CurrentCatalogo.objects.all().delete()
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [CurrentCatalogo])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)
