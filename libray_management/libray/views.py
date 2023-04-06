from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView,CreateView
from .models import User
from .forms import UserForm,AddBook
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.urls import reverse,reverse_lazy
from django.contrib.auth import authenticate,login
from django.contrib import messages

class Home(TemplateView):
    template_name ="home.html"

class Login(LoginView):
    '''login class '''
    template_name = 'login.html'

    # def dispatch(self, request, *args, **kwargs):
    #     username = request.GET.get("username")
    #     password = request.GET.get("password")
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         if user.is_acctive:
    #             login(request,user)
    #     return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # print(request.POST)
            print(request)
            return JsonResponse({"message":"success"})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        # print("username",username," password",password)
        user =  authenticate(username= username, password=password)
        print(user)
        if user is not None  and user.is_active:
            print("inside user",user)
            login(request,user)
            return JsonResponse({"message":"success"})
        return JsonResponse({"error":"user not found."})




        # if request.user.is_authenticated :
        #     print("post request++++++++++++",request.POST)
        # return super().get(request, *args, **kwargs)

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
            user = user_form.save(commit=False)
            user.save()
            messages.success(self.request,"successfully register.")
            return JsonResponse({"message":"success"})
        
        # else:
        #     messages.error(self.request, 'You are already register.')
        return JsonResponse({"error":"user not found."})

class AddBooks(CreateView):
    '''add book'''
    template_name = "add_book.html"
    form_class =AddBook

    def post(self, request, *args, **kwargs):
        book_form = self.form_class(request.POST or None)
        # print(book_form)
        if book_form.is_valid():
            # book = book_form.save(commit=False)
            book_form.save()
            messages.success(self.request,"successfully Add book.")
            
            return JsonResponse({"message":"success"})
        return JsonResponse({"error":"user not found."})

class SuccessMessage(TemplateView):
    template_name = 'successpage.html'