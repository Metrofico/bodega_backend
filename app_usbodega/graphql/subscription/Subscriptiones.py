import graphene

from app_usbodega.graphql.subscription.ConvirtiendoCatalogoSubscription import ConvirtiendoCatalogoSubscription
from app_usbodega.graphql.subscription.NotificacionesSubscription import NotificacionesSubscription
from app_usbodega.graphql.subscription.PersonalNotificacionesSubscription import PersonalNotificacionesSubscription
from .CatalogoSubscription import CatalogoSuscription


class Subscriptiones(graphene.ObjectType):
    catalogo_status = CatalogoSuscription.Field()
    general_notificaciones = NotificacionesSubscription.Field()
    convirtiendo_catalogo_subscription = ConvirtiendoCatalogoSubscription.Field()
    personal_notificaciones = PersonalNotificacionesSubscription.Field()
