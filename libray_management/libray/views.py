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
            # print("inside user",user)
            login(request,user)
            messages.success(self.request,"successfully login")
            return JsonResponse({"message":"success"})
        
        elif user is None:
            messages.error(self.request,"username and password not match.")
            return JsonResponse({"message":"error"})

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
        messages.error(self.request,"username is already registered.")
        
        return JsonResponse({"error":"user not found."})

class AddBooks(LoginRequiredMixin,MyCustomPermissions,CreateView):
    '''add book'''
    login_url = 'login'
    template_name = "add_book.html"
    form_class =AddBook
    permission_required  = {
        "GET": ["libray.add_book"]
    }

    def post(self, request, *args, **kwargs):
        book_form = self.form_class(request.POST or None)
        # print(book_form)
        if book_form.is_valid():
            # book = book_form.save(commit=False)
            book_form.save()
            messages.success(self.request,"successfully Add book.")

            return JsonResponse({"message":"success"})
        print("fnvdvdfvb")
        messages.error(self.request,"You are not authoricesd.")
        return JsonResponse({"error":"user not found."})

class SuccessMessage(TemplateView):
    template_name = 'successpage.html'

# class RegisterUserList(ListView):
#     model = User
#     template_name = 'register_list.html'

#     def post(self,request,*args,**kwargs):
#         user_list = User.objects.all()
#         print(user_list)
#         messages.error(request=self.request, message="You are not authoricesd.")
#         return JsonResponse({"message":"success"})