from datetime import date

from django.core.exceptions import ValidationError
from django.forms import Form, CharField, DateField, ModelChoiceField, Textarea, ModelForm, NumberInput

from viewer.models import Country, Creator, Movie, Genre


class GenreModelForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class CountryModelForm(ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class MovieModelForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


class CreatorModelForm(ModelForm):
    class Meta:
        model = Creator
        fields = '__all__'
        #fields = ['surname', 'name', 'date_of_birth', 'date_of_death']
        #exclude = ['date_of_death', 'name']

    date_of_death = DateField(required=False, widget=NumberInput(attrs={'type': 'date'}))
    date_of_birth = DateField(required=False, widget=NumberInput(attrs={'type': 'date'}))

    def clean_name(self):
        cleaned_data = super().clean()
        initial = cleaned_data['name']
        print(f"initial name: '{initial}'")
        result = initial
        if initial is not None:
            result = initial.strip()
            print(f"result: '{result}'")
            if len(result):
                result = result.capitalize()
            print(f"result: '{result}'")
        return result

    def clean_date_of_birth(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data['date_of_birth']
        if date_of_birth and date_of_birth >= date.today():
            raise ValidationError('Lze zadávat datum narození pouze v minulosti')
        return date_of_birth

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']
        surname = cleaned_data['surname']
        if name is None:
            name = ''
        if surname is None:
            surname = ''
        if len(name.strip()) == 0 and len(surname.strip()) == 0:
            raise ValidationError('Je potřeba zadat jméno nebo příjmení')
        # TODO: pokud jsou zadaná data narození a úmrtí, tak datum narození musí být < datum úmrtí
        cleaned_data['name'] = name
        cleaned_data['surname'] = surname
        return cleaned_data
