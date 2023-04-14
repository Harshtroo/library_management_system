from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView,CreateView,ListView
from .models import User
from .forms import UserForm,AddBook
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.urls import reverse,reverse_lazy
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixin import MyCustomPermissions
from django.contrib.auth.models import Group, User, Permission

class Home(TemplateView):
    template_name ="home.html"

class Login(LoginView):
    '''login class '''
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        # print("username",username," password",password)
        user =  authenticate(username= username, password=password)
        # print(user)
        if user is not None:
            login(request,user)
            # messages.success(self.request,"successfully login")
            return JsonResponse({"message":"success"})
        
        return JsonResponse({"message":"username and password not match."},status=400)

class Logout(LogoutView):
    '''logout class'''
    pass

class CreateUser(CreateView):
    template_name = "create_user.html"
    form_class = UserForm

    def post(self, request, *args, **kwargs):
        '''create user post request'''
        user_form = self.form_class(request.POST or None)

        if user_form.is_valid():
            user = user_form.save()
            user.save()
            user_role = user.role
            group = Group.objects.get(name = user_role)
            user.groups.add(group.id)
            messages.success(self.request,"successfully register.")
            return JsonResponse({"message":"success"})
        # messages.error(self.request,"username is already registered.")
        return JsonResponse({"message":user_form.errors},status=400)


class AddBooks(LoginRequiredMixin,MyCustomPermissions,CreateView):
    '''add book'''
    login_url = 'login'
    template_name = "add_book.html"
    form_class =AddBook
    permission_required  = {
        "GET": ["libray.add_book"]
    }

    def post(self, request, *args, **kwargs):
        book_form = self.form_class(request.POST,request.FILES)
        if book_form.is_valid():
            book_form.save()
            messages.success(request,"successfully add book.")
            return JsonResponse({"message":"success"})
        return JsonResponse({"message":book_form.errors},status=400)


class SuccessMessage(TemplateView):
    """
    
    """
    template_name = 'successpage.html'

