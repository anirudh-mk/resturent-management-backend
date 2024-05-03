from django.urls import path
from . import views

urlpatterns =[
    path("register/", views.CreateUserAPI.as_view()),
    path("login/", views.UserLoginAPI.as_view())

]
