from django.http import HttpResponse
from django.shortcuts import render


def init(request):
    return HttpResponse("Api backend")
