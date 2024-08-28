"""
URL configuration for hollymovies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from viewer.views import hello, hello2, hello3, add, add2

urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello/', hello),
    path('hello2/<str:s>/', hello2),
    path('hello3', hello3),
    path('hello3/', hello3),

    path('add/<int:num1>/<int:num2>/', add),
    path('add2', add2),
]
