import graphene
from graphene_file_upload.scalars import Upload

from app_usbodega import filesutils
from tabula_py import tabula


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
            filesutils.allowextension(ext, "pdf", "txt", "csv")
            namepdf = name + ".pdf"
            namecsv = name + ".csv"
            print("Nombre de archivo: ", namepdf)
            print("Iniciando conversion a csv!: ", namecsv)
            bytess = file.read()
            out_file = open(namepdf, "wb")  # abrir [w]rite as [b]inary
            out_file.write(bytess)
            out_file.close()
            csv = tabula.read_pdf(namepdf, encoding="utf-8", silent=True, pages='all',
                                  java_options=["-Xms4000M", "-Xmx5024M"])
            csv.to_csv(namecsv, encoding="utf-8", index=False)
            print("Conversion completada!")
            success = True
        return Catalogo(success=success)
