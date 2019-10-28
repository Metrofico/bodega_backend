import channels_graphql_ws
import graphene


class CatalogoSuscription(channels_graphql_ws.Subscription):
    done = graphene.String()
    total = graphene.String()
    remaining_time = graphene.String()
    message = graphene.String()

    def subscribe(self, info):
        """
            ESTE METODO ES EJECUTADO CUANDO EL USUARIO SE SUBSCRIBE AL CANAL
        """

        return ["_catalogo_status"]

    def publish(self, info):
        done = self["done"]
        total = self["total"]
        remaining_time = self["remaining_time"]
        message = self["message"]
        """
            ESTE METODO ES EJECUTADO Y DEVUELTO A LOS USUARIOS EN EL CANAL
            Y ES EJECUTADO CUANDO SE EJECUTA EL METODO
            `broadcast` enviando el PAYLOAD Y OBTENIENDOLO CON `self[dato]`
        """
        return CatalogoSuscription(done=done, total=total, remaining_time=remaining_time, message=message)

    @classmethod
    def catalogo_status(cls, done, total, remaining_time, message):
        cls.broadcast(
            group="_catalogo_status",
            payload={"done": done, "total": total, "remaining_time": remaining_time, "message": message},
        )
