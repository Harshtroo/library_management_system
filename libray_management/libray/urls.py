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
    # path('register_user/',views.RegisterUserList.as_view(),name="register_user"),

]

# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
