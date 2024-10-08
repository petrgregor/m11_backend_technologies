# Generated by Django 5.1 on 2024-08-29 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0003_alter_country_options_alter_genre_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name'], 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='creator',
            options={'ordering': ['surname', 'name']},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['title_orig', 'released']},
        ),
    ]
