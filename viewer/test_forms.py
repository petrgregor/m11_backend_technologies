import datetime

from django.test import TestCase

from viewer.forms import CreatorModelForm
from viewer.models import Country


class PeopleFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Country.objects.create(name="Czech", code="CZE")
        Country.objects.create(name="Slovak", code="SK")
        Country.objects.create(name="Germany", code="GER")

    def test_people_form_is_valid(self):
        form = CreatorModelForm(
            data={
                'name': '    martin   ',
                'surname': 'Novák',
                'date_of_birth': '1965-09-17',  #datetime.date(1999, 2, 5).__str__(),
                'date_of_death': '2024-05-05',  #datetime.date(2024,5,5).__str__(),
                'country_of_birth': '1',
                'country_of_death': '',
                'biography': 'Nějaký text'
            }
        )
        print(f"\ntest_people_form_is_valid: {form.data}")
        self.assertTrue(form.is_valid())

    def test_people_date_form_is_invalid(self):
        form = CreatorModelForm(
            data={
                'name': '   martin   ',
                'surname': 'Novák',
                'date_of_birth': '2025-09-17',
                'date_of_death': '1924-05-05',
                'country_of_birth': '2',
                'country_of_death': '',
                'biography': 'Nějaký text'
            }
        )
        print(f"\ntest_people_date_form_is_invalid: {form.data}")
        self.assertFalse(form.is_valid())

# pokud je vazba ManyToMany, pak se zadává seznam: 'genres': ['1', '2']
