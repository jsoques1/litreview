from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import View
from django.conf import settings

from . import forms


@login_required
def home(request):
    # logout(request)
    # return redirect('login')
    return render(request, 'review/home.html')


