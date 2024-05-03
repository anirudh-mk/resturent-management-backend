from django.urls import path

from api.restaurant import views

urlpatterns = [
    path("register/", views.CreateRestaurantAPI.as_view()),
    path("login/", views.RestaurantLoginAPI.as_view()),
]
