import graphene
import tabula
from graphene_file_upload.scalars import Upload

from app_usbodega import filesutils


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
            print("File name: ", name)
            print("Extension: ", ext)
            print("Starting convertions!: ", name)
            bytess = file.read()
            out_file = open(name, "wb")  # open for [w]riting as [b]inary
            out_file.write(bytess)
            out_file.close()
            csv = tabula.read_pdf(name, encoding="utf-8", silent=True,
                                  java_options=["-Dfile.encoding=UTF8", "-Xmx4g"], pages='all')
            csv.to_csv(str(name) + ".csv", encoding="utf-8", index=False)
            print("Sucessful convertions!")
            success = True
        return Catalogo(success=success)
