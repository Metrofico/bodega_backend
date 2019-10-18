import graphene
from graphene_file_upload.scalars import Upload


class Catalogo(graphene.Mutation):
    class Arguments:
        files = Upload()

    success = graphene.Boolean()

    def mutate(self, info, files=None):
        print("Solicitando de client: ", files)
        success = False
        if files is not None:
            for file in files:
                print(file)
                success = True

        return Catalogo(success=success)
