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
from django.db.models import Count


class Home(TemplateView):
    template_name = "home.html"


class Login(LoginView):
    """login class"""

    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
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
    """ success class"""

    template_name = "successpage.html"


class BookList(FormView):
    """ book list show """
    login_url = "login"
    model = Book
    template_name = "book_list.html"
    form_class = AsignBook

    def get(self, request, *args, **kwargs):
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            result = dict()
            data_list = []
            result["status"] = "success"

            for books in Book.objects.all():
                total_books_assign = AssignedBook.objects.filter(book = books).count()
                rem = books.quantity - total_books_assign
                book_list = {
                    "id": books.id,
                    "book_image": books.book_image.url,
                    "book_name": books.book_name,
                    "author_name": books.author_name,
                    "quantity": books.quantity,
                    "available":rem,
                }
                data_list.append(book_list)
            return JsonResponse(data_list,safe=False)
        return render(request, "book_list.html",context={'users':User.objects.all()})

    def post(self, request, *args, **kwargs):
        form = AsignBook(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.POST.get("user"))
            book = Book.objects.get(id=request.POST.get("book"))
            btn_action = request.POST.get('btn_action')

            # if btn_action == 'return_book':
            #     if AssignedBook.objects.filter(book = book,user= user).exists():
            #         AssignedBook.objects.filter(book = book,user= user).delete()
            #         count_assign_book = AssignedBook.objects.filter(book = book).count()
            #         add_book_avl = book.quantity + count_assign_book
            #         return JsonResponse(status=200, data={"message":"successfully book return."})
            #     return JsonResponse(status=400,data={"message":"already book return."})

            if btn_action == 'assign_book':
                if AssignedBook.objects.filter(book = book,user= user).exists():
                    return JsonResponse(status=400,data={"message": "already book assign."})

                assignment = form.save(commit=False)
                assignment.user = user
                assignment.save()

                total_books_assign = AssignedBook.objects.filter(book = book).count()
                rem = book.quantity - total_books_assign
                return JsonResponse({"message":"successfully book assign.","rem":rem,"book_id":book.id})

class AssignBookUser(TemplateView):
    template_name = 'user_assign_book_list.html'
    model = AssignedBook
    
    def get(self, request,*args, **kwargs):
        assign_book_list = list(AssignedBook.objects.filter(user= request.user))
        assign_book_data = [{'id': assign_book.book.id, 'book': assign_book.book.book_name} for assign_book in assign_book_list]
        return JsonResponse(assign_book_data,safe=False)

    # def post(self, request, *args, **kwargs):
    #     user = User.objects.get(id=request.POST.get("user"))
    #     book = Book.objects.get(id=request.POST.get("book"))
        
    #     if btn_action == 'return_book':
    #             if AssignedBook.objects.filter(book = book,user= user).exists():
    #                 AssignedBook.objects.filter(book = book,user= user).delete()
    #                 count_assign_book = AssignedBook.objects.filter(book = book).count()
    #                 add_book_avl = book.quantity + count_assign_book
    #                 return JsonResponse(status=200, data={"message":"successfully book return."})
    #             return JsonResponse(status=400,data={"message":"already book return."})