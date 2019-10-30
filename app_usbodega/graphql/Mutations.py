import graphene

from app_usbodega.Areas import AddArea, DeleteArea, UpdateArea
from app_usbodega.Beneficiario import MutateBeneficiario
from app_usbodega.Cargos import MutateCargo
from app_usbodega.graphql.hibrido.Catalogo import Catalogo
from app_usbodega.graphql.mutations.Categoria import Categoria
from app_usbodega.graphql.mutations.LocalCatalogos import RemoveDataCatalogo
from app_usbodega.graphql.mutations.Register import Register, Logout, AddProducto


class Mutation(graphene.ObjectType):
    register = Register.Field()
    addproducto = AddProducto.Field()
    addcategoria = Categoria.Field()
    addcatalogo = Catalogo.Field()
    logout = Logout.Field()
    addArea = AddArea.Field()
    deleteArea = DeleteArea.Field()
    updateArea = UpdateArea.Field()
    mutateCargo = MutateCargo.Field()
    mutateBeneficiario = MutateBeneficiario.Field()
    removeCatalogo = RemoveDataCatalogo.Field()
