from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=36)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(unique=True, max_length=100)
    profile_pic = models.ImageField(max_length=200, upload_to='user/', null=True, blank=True)
    email = models.CharField(unique=True, max_length=200)
    phone = models.CharField(unique=True, max_length=15)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    @classmethod
    def email_exists(cls, email):
        return cls.objects.filter(email=email).exists()

    class Meta:
        db_table = 'user'


class RestaurantDetails(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=36)
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_detail_restaurant')
    description = models.CharField(max_length=2000, null=True, blank=True)
    location = models.CharField(max_length=2000, null=True, blank=True)
    rating = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'restaurant_details'


class Role(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=36)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role'


class UserRoleLink(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4())
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role_link_role')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_role_link_user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_role_link'
