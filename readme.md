# SDAcademy - PythonRemoteCZ23 - Hollymovies project

## Installation and setup

```bash
pip install django
```

```bash
pip freeze > requirements.txt
```

Create Django project:
```bash
django-admin startproject hollymovies .
```

## Project structure
- hollymovies - settings of our project
  - `__init__.py` - necessary to make this directory as module
  - `asgi.py` - we will not use it
  - `settings.py` - setting of our project
  - `urls.py` - in this file we define url path in our project
  - `wsgi.py` - we will not use it

## Run server
Default on port 8000:
```bash
python manage.py runserver
```

## Tips for Final project
- all installed modules must be in same version for all team members (file requirements.txt)
- `settings.py` - move SECRET_KEY to file ignored by git
