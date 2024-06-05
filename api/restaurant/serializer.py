import uuid

from rest_framework import serializers

from db.models import User, UserRoleLink, RestaurantDetails, RestaurantFoodLink, FoodIngredientsLink, Ingredients, Food


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
        full_name = validated_data['first_name'] + " " + validated_data['last_name']
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
            title=full_name,
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
    category_id = serializers.CharField(source="category.id")
    image = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantFoodLink
        fields = [
            "food_id",
            "title",
            "image",
            "rating",
            "price",
            "is_veg",
            "category_id"
        ]

    def get_image(self, obj):
        return obj.food.profile_pic if obj.food.profile_pic else None


class IngredientsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = [
            "title",
            "description"
        ]

    def create(self, validated_data):
        return Ingredients.objects.create(**validated_data)


class IngredientsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = [
            "id",
            "title",
            "description"
        ]


class FoodCategorySerializer(serializers.ModelSerializer):

    category_id = serializers.CharField(source='category.id')
    title = serializers.CharField(source='category.title')

    class Meta:
        model = RestaurantFoodLink
        fields = [
            "category_id",
            "title"
        ]


class FoodCreateEditDeleteSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.CharField()
    category_id = serializers.CharField()
    price = serializers.CharField()
    is_veg = serializers.CharField()

    class Meta:
        model = Food
        fields = [
            "title",
            "price",
            "is_veg",
            'restaurant_id',
            'category_id'
        ]

    def create(self, validated_data):

        restaurant_id = validated_data['restaurant_id']
        category_id = validated_data['category_id']
        price = validated_data['price']
        is_veg = validated_data['is_veg']

        validated_data['id'] = uuid.uuid4()
        validated_data.pop('price')
        validated_data.pop('is_veg')
        validated_data.pop('restaurant_id')
        validated_data.pop('category_id')

        food = Food.objects.create(**validated_data)

        RestaurantFoodLink.objects.create(
            id=uuid.uuid4(),
            food=food,
            restaurant_id=restaurant_id,
            price=price,
            category_id=category_id,
            is_veg=is_veg
        )

        return food

    def validate(self, data):
        if data.get('title') == 'apple':
            raise serializers.ValidationError('food name already contain')
        return data


class FoodGetSerializer(serializers.ModelSerializer):

    title = serializers.CharField(source="food.title")
    pic = serializers.CharField(source="food.profile_pic")
    description = serializers.CharField(source="food.description")

    class Meta:
        model = RestaurantFoodLink
        fields = [
            "id",
            "title",
            'pic',
            "description",
            "rating",
            "price",
            "is_veg",
        ]
