from django.conf.urls import url

from app_usbodega.CustomViews import SentryGraphQLView

urlpatterns = [
    url(r'^gql', SentryGraphQLView.as_view(graphiql=False, batch=True))
]
