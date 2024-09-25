from datetime import date

from django.db.models import *  # Model, CharField, DateField, ForeignKey, SET_NULL, TextField, ManyToManyField, IntegerField

from accounts.models import Profile


class Genre(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"Genre(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Country(Model):
    name = CharField(max_length=64, null=False, blank=False, unique=True)
    code = CharField(max_length=3, null=False, blank=False, unique=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __repr__(self):
        return f"Country(name={self.name}, code={self.code})"

    def __str__(self):
        return f"{self.name}"


class Creator(Model):
    name = CharField(max_length=32, null=True, blank=True)
    surname = CharField(max_length=32, null=True, blank=True)
    date_of_birth = DateField(null=True, blank=True)
    date_of_death = DateField(null=True, blank=True)
    country_of_birth = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL, related_name='creators_born')
    country_of_death = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL, related_name='creators_died')
    biography = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['surname', 'name']

    def __repr__(self):
        return f"Creator(name={self.name}, surname={self.surname})"

    def __str__(self):
        return f"{self.name} {self.surname}"

    def age(self):
        if self.date_of_birth:
            end_date = date.today()
            if self.date_of_death:
                end_date = self.date_of_death
            return (end_date.year - self.date_of_birth.year -
                    ((end_date.month, end_date.day) < (self.date_of_birth.month, self.date_of_birth.day)))
        return None


class Movie(Model):
    title_orig = CharField(max_length=150, null=False, blank=False)  # https://en.wikipedia.org/wiki/Night_of_the_Day_of_the_Dawn_of_the_Son_of_the_Bride_of_the_Return_of_the_Revenge_of_the_Terror_of_the_Attack_of_the_Evil,_Mutant,_Alien,_Flesh_Eating,_Hellbound,_Zombified_Living_Dead
    title_cz = CharField(max_length=150, null=True, blank=True)
    genres = ManyToManyField(Genre, blank=True, related_name='movies')
    countries = ManyToManyField(Country, blank=True, related_name='movies')
    actors = ManyToManyField(Creator, blank=True, related_name='acting')
    directors = ManyToManyField("viewer.Creator", blank=True, related_name='directing')
    length = IntegerField(null=True, blank=True)  # min
    released = IntegerField(null=True, blank=True)  # year
    description = TextField(null=True, blank=True)
    rating = FloatField(null=True, blank=True)  # 0-100
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title_orig', 'released']

    def __repr__(self):
        return f"Movie(title_orig={self.title_orig})"

    def __str__(self):
        return f"{self.title_orig} ({self.released})"

    def length_format(self):
        hours = self.length // 60
        minutes = self.length % 60
        if minutes < 10:
            minutes = f"0{minutes}"
        return f"{hours}:{minutes}"


class Image(Model):
    image = ImageField(upload_to='images/', default=None, null=False, blank=False)
    movie = ForeignKey(Movie, on_delete=SET_NULL, null=True, blank=True, related_name='images')
    actors = ManyToManyField(Creator, blank=True, related_name='images')
    description = TextField(null=True, blank=True)

    def __repr__(self):
        return f"Image(image={self.image}, movie={self.movie}, actors={self.actors}, description={self.description})"

    def __str__(self):
        return f"Image: {self.image}, {self.description}"


class Review(Model):
    movie = ForeignKey(Movie, on_delete=CASCADE, null=False, blank=False, related_name='reviews')
    user = ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=False, related_name='reviews')
    rating = IntegerField(null=True, blank=True)
    text = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __repr__(self):
        return (f"Review(movie={self.movie}, user={self.user}, "
                f"rating={self.rating}, text={self.text})")

    def __str__(self):
        return f"User: {self.user}, movie:{self.movie}, rating={self.rating}, text={self.text[:50]}"
