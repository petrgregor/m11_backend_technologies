from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView, DetailView

from logging import getLogger

from accounts.models import Profile
from viewer.forms import CreatorModelForm, MovieModelForm, GenreModelForm, CountryModelForm, ImageModelForm, \
    ReviewModelForm
from viewer.models import Movie, Creator, Genre, Country, Image, Review

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


class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.add_movie'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')
    model = Movie
    permission_required = 'viewer.change_movie'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a creator.')
        return super().form_invalid(form)


class MovieDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.delete_movie'


"""def movie(request, pk):
    if Movie.objects.filter(id=pk).exists():
        movie_ = Movie.objects.get(id=pk)
        context = {'movie': movie_}
        return render(request, "movie.html", context)
    return redirect('movies')"""


class MovieTemplateView(TemplateView):
    template_name = "movie.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        review_ = Review.objects.filter(movie=context["movie"], user=Profile.objects.get(user=request.user))
        if review_.exists():
            review_ = Review.objects.get(movie=context["movie"], user=Profile.objects.get(user=request.user))
            review_.rating = request.POST.get("rating")
            review_.text = request.POST.get("text")
            review_.save()
        else:
            Review.objects.create(movie=context["movie"],
                                  user=Profile.objects.get(user=request.user),
                                  rating=request.POST.get("rating"),
                                  text=request.POST.get("text")
                                  )
        # Recalculate the rating for the given movie
        movie_ = context["movie"]
        movie_.rating = movie_.reviews.aggregate(Avg('rating'))['rating__avg']  #Review.objects.filter(movie=movie_).aggregate(Avg('rating'))['rating__avg']
        movie_.save()
        return render(request, "movie.html", context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        movie_ = Movie.objects.get(id=pk)
        context["movie"] = movie_
        context["form_review"] = ReviewModelForm
        return context


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


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class CreatorCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.add_creator'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class CreatorUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')
    model = Creator
    permission_required = 'viewer.change_creator'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a creator.')
        return super().form_invalid(form)


class CreatorDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Creator
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.delete_creator'


class GenreView(View):
    def get(self, request, pk):
        genres = Genre.objects.all()
        genre = Genre.objects.get(id=pk)
        movies = Movie.objects.filter(genres__id=pk)
        countries = Country.objects.all()
        context = {'genres': genres, 'genre': genre, 'movies': movies,
                   'countries': countries}
        return render(request, "movies.html", context)


class GenresListView(ListView):
    template_name = "genres.html"
    model = Genre
    context_object_name = 'genres'


class GenreCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = GenreModelForm
    success_url = reverse_lazy('home')
    permission_required = 'viewer.add_genre'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class GenreUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = GenreModelForm
    success_url = reverse_lazy('home')
    model = Genre
    permission_required = 'viewer.change_genre'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a creator.')
        return super().form_invalid(form)


class GenreDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Genre
    success_url = reverse_lazy('home')
    permission_required = 'viewer.delete_genre'


class CountryView(View):
    def get(self, request, pk):
        genres = Genre.objects.all()
        countries = Country.objects.all()
        country = Country.objects.get(id=pk)
        movies = Movie.objects.filter(countries=country)
        context = {'genres': genres, 'countries': countries, 'movies': movies, 'country': country}
        return render(request, "movies.html", context)


class CountriesListView(ListView):
    template_name = "countries.html"
    model = Country
    context_object_name = 'countries'


class CountryCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('home')
    permission_required = 'viewer.add_country'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class CountryUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('home')
    model = Country
    permission_required = 'viewer.change_country'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a creator.')
        return super().form_invalid(form)


class CountryDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Country
    success_url = reverse_lazy('home')
    permission_required = 'viewer.delete_country'


class ProfilesListView(ListView):
    template_name = "profiles.html"
    model = Profile
    context_object_name = 'profiles'


class ImageCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form_image.html'
    form_class = ImageModelForm
    success_url = reverse_lazy('home')
    permission_required = 'viewer.add_image'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class ImageUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form_image.html'
    form_class = ImageModelForm
    success_url = reverse_lazy('images')
    model = Image
    permission_required = 'viewer.change_image'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a creator.')
        return super().form_invalid(form)


class ImageDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Image
    success_url = reverse_lazy('images')
    permission_required = 'viewer.delete_image'


class ImageDetailView(DetailView):
    model = Image
    template_name = 'image.html'


class ImagesListView(ListView):
    template_name = "images.html"
    model = Image
    context_object_name = 'images'


class ReviewDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Review
    success_url = reverse_lazy('movies')

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        movie_ = self.object.movie

        response = super().delete(request, *args, **kwargs)

        average_rating = movie_.reviews.aggregate(Avg('rating'))['rating__avg']

        movie_.rating = average_rating
        movie_.save()
        print(movie_)

        return response


    """def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return referer
        return super().get_success_url()"""