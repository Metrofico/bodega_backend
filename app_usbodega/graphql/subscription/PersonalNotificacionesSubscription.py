import channels_graphql_ws
import graphene


class PersonalNotificacionesSubscription(channels_graphql_ws.Subscription):
    status = graphene.String()
    mensaje = graphene.String()

    def subscribe(self, info):
        user_id = info.context.userId
        return [user_id]

    def publish(self, info):
        status = self["status"]
        mensaje = self["mensaje"]
        return PersonalNotificacionesSubscription(status=status, mensaje=mensaje)

    @classmethod
    def enviar_notificacion(cls, user_id, status, mensaje):
        cls.broadcast(
            group=user_id,
            payload={"status": status, "mensaje": mensaje},
        )
