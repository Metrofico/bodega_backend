from django.http import HttpResponse


def init(request):
    return HttpResponse("Api backend")
