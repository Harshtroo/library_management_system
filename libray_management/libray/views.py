from typing import Any
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView,FormView
from .models import User, Book,AssignedBook
from .forms import UserForm, AddBook,  AsignBook
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixin import MyCustomPermissions
from django.contrib.auth.models import Group, Permission
from django.core import serializers
from django.conf import settings
# import json


class Home(TemplateView):
    template_name = "home.html"


class Login(LoginView):
    """login class"""

    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        # print("username",username," password",password)
        user = authenticate(username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            # messages.success(self.request,"successfully login")
            return JsonResponse({"message": "success"})

        return JsonResponse({"message": "username and password not match."}, status=400)


class Logout(LogoutView):
    """logout class"""

    pass


class CreateUser(CreateView):
    template_name = "create_user.html"
    form_class = UserForm

    def post(self, request, *args, **kwargs):
        """create user post request"""
        user_form = self.form_class(request.POST or None)

        if user_form.is_valid():
            user = user_form.save()
            user.save()
            user_role = user.role
            group = Group.objects.get(name=user_role)
            user.groups.add(group.id)
            messages.success(self.request, "successfully register.")
            return JsonResponse({"message": "success"})
        return JsonResponse({"message": user_form.errors}, status=400)


class AddBooks(LoginRequiredMixin, MyCustomPermissions, CreateView):
    """add book"""

    login_url = "login"
    template_name = "add_book.html"
    form_class = AddBook
    permission_required = {"GET": ["libray.add_book"]}

    def post(self, request, *args, **kwargs):
        book_form = self.form_class(request.POST, request.FILES)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.available_quantity = book_form.cleaned_data.get("quantity")
            book.save()
            messages.success(request, "successfully add book.")
            return JsonResponse({"message": "success"})
        return JsonResponse({"message": book_form.errors}, status=400)


class SuccessMessage(TemplateView):
    """ """

    template_name = "successpage.html"


class BookList(FormView):
    login_url = "login"
    model = Book
    template_name = "book_list.html"
    form_class = AsignBook

    def get(self, request, *args, **kwargs):
        # print("user===============",User.objects.all())
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            result = dict()
            data_list = []
            result["status"] = "success"
            for books in Book.objects.all():
                book_list = {
                    "id": books.id,
                    "book_image": books.book_image.url,
                    "book_name": books.book_name,
                    "author_name": books.author_name,
                    "quantity": books.quantity,
                    "available":books.available_quantity,
                }
                data_list.append(book_list)
            # result["data"] = data_list
            return JsonResponse(data_list,safe=False)
        return render(request, "book_list.html",context={'users':User.objects.all()})

    def post(self, request, *args, **kwargs):

        get_user_id = request.POST.getlist("user_id[]")
        get_book_id = request.POST.get("book_id")

        book_obj = Book.objects.filter(id=get_book_id).first()
        assigned_book = AssignedBook.objects.create(book=book_obj)

        if AssignedBook.objects.filter(book = book_obj,user__in=get_user_id).exists():
            return JsonResponse(status=400,data={"message": "error"})
        # avl_qu = book_obj.quantity - len(get_user_id)
        # avl_qu.save()
        # breakpoint()

        setattr(book_obj,"available_quantity", book_obj.available_quantity - len(get_user_id))
        book_obj.save()
        
        assigned_book.user.set(get_user_id)
        print("total",book_obj.quantity)

        
        
        return JsonResponse({"message":"success"})
