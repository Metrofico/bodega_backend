import channels_graphql_ws
import graphene


class NotificacionesSubscription(channels_graphql_ws.Subscription):
    status = graphene.String()
    mensaje = graphene.String()

    def subscribe(self, info):
        return ["_notificaciones_generales"]

    def publish(self, info):
        status = self["status"]
        mensaje = self["mensaje"]
        return NotificacionesSubscription(status=status, mensaje=mensaje)

    @classmethod
    def enviar_notificacion(cls, status, mensaje):
        cls.broadcast(
            group="_notificaciones_generales",
            payload={"status": status, "mensaje": mensaje},
        )
