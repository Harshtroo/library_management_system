from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import User
from django.contrib.auth.views import LoginView

class Home(TemplateView):
    template_name ="home.html"

class Login(LoginView):
    '''login class '''
    template_name = 'login.html'
    
    