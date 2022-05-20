from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import View
from django.conf import settings

from . import forms


def home(request):
    logout(request)
    return redirect('login')


