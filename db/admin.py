from django.contrib import admin
from .models import User, RestaurantDetails, Role, UserRoleLink, Food, RestaurantFoodLink, Ingredients, FoodIngredientsLink, Category, FoodCategoryLink


class UserModel(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'created_at')
    search_fields = ('id', 'first_name', 'last_name', 'username', 'email', 'created_at')


admin.site.register(User, UserModel)


class RestaurantModel(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'description', 'location', 'rating', 'created_at')
    search_fields = ('id', 'restaurant', 'description', 'location', 'rating', 'created_at')


admin.site.register(RestaurantDetails, RestaurantModel)


class RoleModel(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('id', 'title', 'created_at')


admin.site.register(Role, RoleModel)


class UserRoleLinkModel(admin.ModelAdmin):
    list_display = ('id', 'role', 'user', 'created_at')
    search_fields = ('id', 'role', 'user', 'created_at')


admin.site.register(UserRoleLink, UserRoleLinkModel)


class FoodModel(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'profile_pic', 'created_at')
    search_fields = ('id', 'title', 'description', 'created_at')


admin.site.register(Food, FoodModel)


class RestaurantFoodLinkModel(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'food', 'rating', 'price', 'created_at')
    search_fields = ('id', 'restaurant', 'food', 'rating', 'price', 'created_at')


admin.site.register(RestaurantFoodLink, RestaurantFoodLinkModel)


class IngredientsModel(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at')
    search_fields = ('id', 'title', 'description', 'created_at')


admin.site.register(Ingredients, IngredientsModel)


class FoodIngredientsLinkModel(admin.ModelAdmin):
    list_display = ('id', 'food', 'ingredients', 'created_at')
    search_fields = ('id', 'food', 'ingredients', 'created_at')


admin.site.register(FoodIngredientsLink, FoodIngredientsLinkModel)


class CategoryModel(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('id', 'title', 'created_at')


admin.site.register(Category, CategoryModel)


class FoodCategoryLinkModel(admin.ModelAdmin):
    list_display = ('id', 'food', 'category', 'created_at')
    search_fields = ('id', 'food', 'category', 'created_at')


admin.site.register(FoodCategoryLink, FoodCategoryLinkModel)
