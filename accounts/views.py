from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import SignUpForm


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


@login_required
def user_logout(request):
    logout(request)
    #return render(request, 'home.html')
    return redirect(request.META.get('HTTP_REFERER', '/'))  # zůstat na stejné stránce
