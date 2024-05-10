from django.urls import path

from api.restaurant import views

urlpatterns = [
    path("register/", views.CreateRestaurantAPI.as_view()),
    path("login/", views.RestaurantLoginAPI.as_view()),
    path("list/", views.RestaurantListAPI.as_view()),
    path("food-list/<str:restaurant_id>/", views.RestaurantFoodListAPI.as_view()),
    path("create/ingredients/", views.IngredientsCreateAPI.as_view()),
    path("ingredients/list/", views.IngredientsListAPI.as_view()),
]
