from django.contrib import admin
from django.urls import path
# import .views
from libray import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.Home.as_view(),name="home"),
    path('login/',views.Login.as_view(),name="login"),
]
