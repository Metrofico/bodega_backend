import json
import re
from datetime import datetime

import graphene
from django.conf import settings
from django.core.management.color import no_style
from django.db import connection
from graphene_file_upload.scalars import Upload

from app_usbodega import filesutils
from tabula_py import tabula
from .ObjectsTypes import CatalogoType, CatalogoUpdateCurrent
from .models import Catalogos, CurrentCatalogo

ID_DE_EXISTENCIA = "ID EXISTENCIA"
DESCRIPCION = "DESCRIPCION"


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
            raise Exception("No hay datos para importar")
        try:
            catalogo_object = Catalogos.objects.get(nameFile=catalogo + ".pdf")
        except Exception:
            raise Exception("No existe un catalogo con ese nombre")
        csvpath = catalogo_object.file
        csvpath = csvpath.replace("{BODEGA_FOLDER}", settings.BODEGA_FOLDER)
        csvpath = csvpath.replace("{DB_FILES_STATIC}", settings.DB_FILES_STATIC)
        print(csvpath)
        input_file = open("." + csvpath, "r")
        csvcontent = input_file.read()
        processjson(csvcontent)
        return CatalogoUpdateCurrent(success=csvcontent)


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
    datas = json.loads(jsoncontent)
    count = 0
    total = len(datas)
    print("Iniciando proceso de registro de catalogo: " + str(total))
    for element in datas:
        if count is 0:
            count = count + 1
            continue

        id_existencia = str(element["ID EXISTENCIA"])
        descripcion = str(element["Unnamed: 1"])

        # 2901000029000176
        # 1302000013001109
        # 902000009000032
        # 1801000018001623
        # 1801000018001405

        # BUSCAR Y CORREGIR ESE PROBLEMA
        # 1302000013003748
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
        descripcion = replace_last_word(descripcion, "UNIDAD")
        dic_descripcion = extract_code_from_description(descripcion)
        if not dic_descripcion["code"] is None:
            item_presu = dic_descripcion["code"]
            descripcion = dic_descripcion["newtext"]
        current_catalogo = CurrentCatalogo(id_de_existencia=id_existencia, descripcion=descripcion,
                                           item_presupuestario=item_presu)
        current_catalogo.save()
        print("Procesando elemento de catalogo " + str(count) + "/" + str(total))
        count = count + 1

    print("Cátalogo ha sido procesado correctamente")
    pass


class Catalogo(graphene.Mutation):
    class Arguments:
        file = Upload()

    success = graphene.Boolean()

    def mutate(self, info, file=None):
        success = False
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
            print("Iniciando conversion a json!: ", namejson)
            filesutils.allowextension(ext, "pdf")
            dbfiles_out_csv = "./" + settings.DB_FILES_STATIC + "/" + settings.BODEGA_FOLDER + "/" + namejson
            dbfiles_out_pdf = "./" + settings.DB_FILES_STATIC + "/" + settings.BODEGA_FOLDER + "/" + namepdf
            dbfiles_out_replazable = "./" + "{DB_FILES_STATIC}" + "/{BODEGA_FOLDER}/" + namejson
            bytess = file.read()
            out_file = open(dbfiles_out_pdf, "wb")  # archivo [w]rite(escribir) como [b]inary(binario)
            out_file.write(bytess)
            out_file.close()
            csv = tabula.read_pdf(dbfiles_out_pdf, encoding="utf-8", silent=True, pages='all',
                                  java_options=["-Xms3000M", "-Xmx3024M"])
            csv.to_json(dbfiles_out_csv, orient="records", index=True)
            # input_file = open(dbfiles_out_csv, "r")
            # csvcontent = input_file.read()
            # processjson(csvcontent)
            catalogo = Catalogos(nameFile=namepdf, file=dbfiles_out_replazable[1:], date_uploaded=date)
            catalogo.save()
            print("Conversion completada!")
            success = True
        return Catalogo(success=success)


def resetSql():
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [CurrentCatalogo])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)
