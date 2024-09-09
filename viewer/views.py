from django.http import HttpResponse
from django.shortcuts import render

from viewer.models import Movie, Creator


def home(request):
    return render(request, "home.html")


def movies(request):
    movies_ = Movie.objects.all()
    context = {'movies': movies_}
    return render(request, "movies.html", context)


def creators(request):
    creators_ = Creator.objects.all()
    context = {'creators': creators_}
    return render(request, "creators.html", context)
