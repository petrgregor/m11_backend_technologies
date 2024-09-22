import datetime

from django.test import TestCase

from viewer.models import Movie, Country, Creator, Genre


class MovieModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        movie = Movie.objects.create(
            title_orig="Originální název filmu",
            title_cz="Český název filmu",
            length=123,
            rating=85,
            released=2010,
            description="Popis filmu"
        )

        country_cz = Country.objects.create(name="Czech", code="CZE")
        #Country.objects.create(name="Czech")
        country_sk = Country.objects.create(name="Slovak", code="SK")
        movie.countries.add(country_cz)
        movie.countries.add(country_cz)
        movie.countries.add(country_sk)

        director = Creator.objects.create(
            name="Arnošt",
            surname="Novák",
            date_of_birth=datetime.date(1975, 12, 10),
            country_of_birth=country_cz,
            biography="Režíroval několik filmů"
        )
        movie.directors.add(director)

        actor1 = Creator.objects.create(
            name="Bedřich",
            surname="Slováček",
            date_of_birth=datetime.date(1969, 11, 5),
            country_of_birth=country_cz,
            biography="Mizerný herec"
        )
        movie.actors.add(actor1)

        actor2 = Creator.objects.create(
            name="Cyril",
            surname="Novotný",
            date_of_birth=datetime.date(1985, 4, 5),
            country_of_birth=country_sk,
            biography="Skvělý herec"
        )
        movie.actors.add(actor2)

        genre_drama = Genre.objects.create(name="Drama")
        movie.genres.add(genre_drama)
        genre_comedy = Genre.objects.create(name="Komedie")
        movie.genres.add(genre_comedy)
        # Genre.objects.create(name="Drama")

        movie.save()

    def setUp(self):
        print('-'*80)

    def test_title_orig(self):
        movie = Movie.objects.get(id=1)
        print(f"test_title_orig: '{movie.title_orig}'")
        self.assertEqual(movie.title_orig, "Originální název filmu")

    def test_movie_repr(self):
        movie = Movie.objects.get(id=1)
        print(f"test_movie_repr: '{movie.__repr__()}'")
        self.assertEqual(movie.__repr__(), "Movie(title_orig=Originální název filmu)")

    def test_movie_str(self):
        movie = Movie.objects.get(id=1)
        print(f"test_movie_str: '{movie}'")
        self.assertEqual(movie.__str__(), "Originální název filmu (2010)")

    def test_movie_countries_count(self):
        movie = Movie.objects.get(id=1)
        number_of_countries = movie.countries.count()
        print(f"test_movie_countries_count: {number_of_countries}")
        self.assertEqual(number_of_countries, 2)

    def test_country_unique(self):
        czech_countries = Country.objects.filter(name="Czech").count()
        print(f"test_country_unique: Czech={czech_countries}")
        self.assertEqual(czech_countries, 1)

    def test_genre_unique(self):
        genre_count = Genre.objects.filter(name="Drama").count()
        print(f"test_genre_unique: Czech={genre_count}")
        self.assertEqual(genre_count, 1)
