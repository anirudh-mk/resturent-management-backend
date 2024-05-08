import uuid

from rest_framework import serializers

from db.models import User, UserRoleLink, RestaurantDetails, RestaurantFoodLink, FoodIngredientsLink


class RestaurantCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    location = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "confirm_password",
            "description",
            "location",
        ]

    def create(self, validated_data):

        description = validated_data['description']
        location = validated_data['location']

        validated_data['id'] = uuid.uuid4()
        validated_data['username'] = validated_data['email']
        validated_data.pop('confirm_password')
        validated_data.pop('location')
        validated_data.pop('description')

        user = User.objects.create_user(**validated_data)

        UserRoleLink.objects.create(
            id=uuid.uuid4(),
            role_id=self.context.get("role_id"),
            user=user
        )

        RestaurantDetails.objects.create(
            id=uuid.uuid4(),
            restaurant=user,
            description=description,
            location=location,
        )

        return user

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('Passwords do not match')
        return data


class RestaurantListSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.CharField(source="restaurant.id")
    title = serializers.SerializerMethodField()
    email = serializers.CharField(source="restaurant.email")
    phone = serializers.CharField(source="restaurant.phone")
    profile_pic = serializers.CharField(source="restaurant.profile_pic")

    class Meta:
        model = RestaurantDetails
        fields = [
            "restaurant_id",
            "title",
            "email",
            "phone",
            "profile_pic",
            "description",
            "location",
            "rating"
        ]

    def get_title(self, obj):
        if not obj.restaurant.last_name:
            return obj.restaurant.first_name
        return obj.restaurant.first_name + " " + obj.restaurant.last_name


class RestaurantFoodListSerializer(serializers.ModelSerializer):
    food_id = serializers.CharField(source="food.id")
    title = serializers.CharField(source="food.title")
    image = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantFoodLink
        fields = [
            "food_id",
            "title",
            "image",
            "description",
            "rating",
            "price",
            "ingredients"
        ]

    def get_image(self, obj):
        return obj.food.profile_pic if obj.food.profile_pic else None

    def get_description(self, obj):
        return obj.food.description if obj.food.description else None

    def get_ingredients(self, obj):

        food_ingredients_list = FoodIngredientsLink.objects.filter(
            food=obj.food).values_list(
            'ingredients__title',
            flat=True
        )
        return food_ingredients_list
