import channels_graphql_ws
import graphene

from app_usbodega import utils
from app_usbodega.graphql.Mutations import Mutation
from app_usbodega.graphql.Querys import Query
from app_usbodega.graphql.subscription.Subscriptiones import Subscriptiones


class Mutations(Mutation, graphene.ObjectType):
    pass


class Querys(Query, graphene.ObjectType):
    pass


class Subscription(Subscriptiones, graphene.ObjectType):
    pass


def get_cookies_from_header(headers):
    cookies_get = {}
    for h in headers:
        key = str(h[0], "utf8")
        if key == "cookie":
            cookies = str(h[1], "utf8").split(";")
            for cookie in cookies:
                cookie = cookie.strip().split("=")
                key = cookie[0]
                value = cookie[1]
                cookies_get[key] = value
    return cookies_get


def middleware_onlysubscription(next_middleware, root, info, *args, **kwds):
    if info.operation.name is not None and info.operation.name.value != "IntrospectionQuery":
        if info.operation.operation != "subscription":
            raise Exception("Only support subscription")
    cookies = get_cookies_from_header(info.context.headers)
    if "oAtmp" in cookies:
        user_decoded = utils.logindecode(cookies["oAtmp"])
        if user_decoded:
            # PROCESO DE VERIFICACION
            pass
        else:
            raise Exception("No autorizado")
    else:
        raise Exception("No autorizado")
    return next_middleware(root, info, *args, **kwds)


schema_querys = graphene.Schema(query=Querys, mutation=Mutations,
                                auto_camelcase=False)


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""
    schema = graphene.Schema(query=Querys, mutation=Mutations, subscription=Subscription,
                             auto_camelcase=False)

    # Uncomment to send keepalive message every 42 seconds.
    # send_keepalive_every = 40

    # Uncomment to process requests sequentially (useful for tests).
    # strict_ordering = True

    async def on_connect(self, payload):
        """New client connection handler."""
        # You can `raise` from here to reject the connection.
        # Payload viene los datos del usuario
        # print("Payload: ", payload)
        # if "oAtmp" in payload:
        #     if not str(payload["oAtmp"]).strip() or payload["oAtmp"] is None:
        #         raise Exception("Not allowed")
        # self.scope["token"] = payload["oAtmp"]
        cookies = get_cookies_from_header(self.scope["headers"])
        user_decoded = utils.logindecode(cookies["oAtmp"])
        if user_decoded:
            self.scope["userId"] = user_decoded.get("id")
            print("Usuario: " + user_decoded.get("id"))
        print("Cliente detectado: ", payload, " cookies: ", cookies)

    middleware = [middleware_onlysubscription]
