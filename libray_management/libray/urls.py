from django.contrib import admin
from django.urls import path
# import .views
from libray import views
from django.conf import settings
from django.conf.urls.static import static  

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.Home.as_view(),name="home"),
    path('login/',views.Login.as_view(),name="login"),
    path('logout/',views.Logout.as_view(),name="logout"),
    path('create_user/',views.CreateUser.as_view(),name="create_user"),
    path('add_book/',views.AddBooks.as_view(),name="add_book"),
    path('success_register/',views.SuccessMessage.as_view(),name="success_register"),
    path('book_list/',views.BookList.as_view(),name="book_list"),
]

