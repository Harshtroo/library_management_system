from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView
from .models import User, Book
from .forms import UserForm, AddBook
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.http import HttpResponse, JsonResponse
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
            book_form.save()
            messages.success(request, "successfully add book.")
            return JsonResponse({"message": "success"})
        return JsonResponse({"message": book_form.errors}, status=400)


class SuccessMessage(TemplateView):
    """ """

    template_name = "successpage.html"


class BookList(ListView):
    login_url = "login"
    model = Book
    template_name = "book_list.html"

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
                }
                data_list.append(book_list)
            # result["data"] = data_list
            return JsonResponse(data_list,safe=False)
        
        return render(request, "book_list.html",context={'users':User.objects.all()})

    # def get_context_data(self, **kwargs):
        
    #     users = User.objects.all()
    #     user_data = [{'username': user.username, 'email': user.email} for user in users]
    #     return JsonResponse(user_data, safe=False)
    
    
# class AssignBook(ListView):
#     model = User
#     template_name = "assign_book.html"

#     def get(self, request, *args, **kwargs):
#         # if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         #     result = dict()
#         #     user_list = []
#         #     result['status']="success"
#         #     for users in User.objects.all():
#         #         user_list.append(users)
#         #     result['data'] = user_list
#         #     # user = settings.AUTH_USER_MODEL
#         #     return JsonResponse(user_list,safe=False)
#         # return render(request,'assign_book.html')
#         print("dvdfin")
#         # breakpoint()
#         user = User.objects.get()
#         return JsonResponse(user, safe=False)
