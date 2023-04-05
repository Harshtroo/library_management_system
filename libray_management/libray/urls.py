from django.contrib import admin
from django.urls import path
# import .views
from libray import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.Home.as_view(),name="home"),
    path('login/',views.Login.as_view(),name="login"),
    path('logout/',views.Logout.as_view(),name="logout"),
    path('create_user/',views.CreateUser.as_view(),name="create_user"),

]

