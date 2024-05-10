from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.restaurant.serializer import RestaurantCreateSerializer, RestaurantListSerializer, \
    RestaurantFoodListSerializer, IngredientsCreateSerializer, IngredientsListSerializer
from db.models import Role, UserRoleLink, RestaurantDetails, RestaurantFoodLink, Ingredients
from utils.permissions import TokenGenerate, CustomizePermission, role_required
from utils.response import CustomResponse
from utils.types import RoleType


class CreateRestaurantAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        role_id = Role.objects.filter(title='RESTAURANT').first().id
        serializer = RestaurantCreateSerializer(
            data=request.data,
            context={
                "role_id": role_id
            }
        )
        if serializer.is_valid():
            serializer.save()

            return CustomResponse(
                general_message='Restaurant created successfully'
            ).get_success_response()

        return CustomResponse(
            response=serializer.errors
        ).get_failure_response()


class RestaurantLoginAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return CustomResponse(
                general_message='email and password is required'
            ).get_failure_response()

        user = authenticate(request, email=email, password=password)
        if user:
            role = UserRoleLink.objects.filter(user=user).first().role.title
            auth = TokenGenerate().generate(user, role)
            return CustomResponse(
                general_message="successfully login",
                response=auth,
            ).get_success_response()
        else:
            return CustomResponse(
                general_message="login failed"
            ).get_failure_response()


class RestaurantListAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        restaurant_details = RestaurantDetails.objects.all()

        serializer_data = RestaurantListSerializer(
            restaurant_details,
            many=True
        ).data
        return CustomResponse(response=serializer_data).get_success_response()


class RestaurantFoodListAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, restaurant_id):
        restaurant_food_link = RestaurantFoodLink.objects.filter(restaurant=restaurant_id).all()

        serializer = RestaurantFoodListSerializer(
            restaurant_food_link,
            many=True
        )

        return CustomResponse(response=serializer.data).get_success_response()


class IngredientsCreateAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = IngredientsCreateSerializer(
            data=request.data
        )
        if serializer.is_valid():
            ingredients = serializer.save()

            return CustomResponse(
                general_message=f'{ingredients.title} added to ingredients',
            ).get_success_response()

        return CustomResponse(response=serializer.errors).get_failure_response()


class IngredientsListAPI(APIView):
    authentication_classes = [CustomizePermission]

    @role_required(RoleType.RESTAURANT.value,)
    def get(self, request):
        ingredients = Ingredients.objects.all()
        serializer = IngredientsListSerializer(
            ingredients,
            many=True
        )

        return CustomResponse(response=serializer.data).get_failure_response()
