from django.urls import path
from .views import register,loginPage,logoutPage
urlpatterns = [
    path("register/",register,name="register"),
    path("login/",loginPage,name="login"),
    path("logout/",logoutPage,name="logout"),
]
