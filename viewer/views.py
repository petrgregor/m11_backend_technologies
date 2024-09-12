from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from logging import getLogger

from viewer.forms import CreatorModelForm
from viewer.models import Movie, Creator, Genre, Country


LOGGER = getLogger()


def home(request):
    return render(request, "home.html")


class MoviesListView(ListView):
    template_name = "movies.html"
    model = Movie
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = Genre.objects.all()
        context['genres'] = genres
        context['countries'] = Country.objects.all()
        context['movies'] = Movie.objects.all()
        return context


def movie(request, pk):
    if Movie.objects.filter(id=pk).exists():
        movie_ = Movie.objects.get(id=pk)
        context = {'movie': movie_}
        return render(request, "movie.html", context)
    return redirect('movies')


class CreatorsListView(ListView):
    template_name = "creators.html"
    model = Creator
    context_object_name = 'creators'


#@login_required
def creator(request, pk):
    if Creator.objects.filter(id=pk).exists():
        creator_ = Creator.objects.get(id=pk)
        return render(request, "creator.html", {'creator': creator_})
    return redirect('creators')


class CreatorCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class CreatorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')
    model = Creator

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a creator.')
        return super().form_invalid(form)


class CreatorDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Creator
    success_url = reverse_lazy('creators')


class GenreView(View):
    def get(self, request, pk):
        genres = Genre.objects.all()
        genre = Genre.objects.get(id=pk)
        movies = Movie.objects.filter(genres__id=pk)
        countries = Country.objects.all()
        context = {'genres': genres, 'genre': genre, 'movies': movies,
                   'countries': countries}
        return render(request, "movies.html", context)


class CountryView(View):
    def get(self, request, pk):
        genres = Genre.objects.all()
        countries = Country.objects.all()
        country = Country.objects.get(id=pk)
        movies = Movie.objects.filter(countries=country)
        context = {'genres': genres, 'countries': countries, 'movies': movies, 'country': country}
        return render(request, "movies.html", context)

