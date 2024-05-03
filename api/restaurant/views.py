from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.restaurant.serializer import RestaurantCreateSerializer
from db.models import Role, UserRoleLink
from utils.permissions import TokenGenerate
from utils.response import CustomResponse


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
            user_role_title = UserRoleLink.objects.filter(user=user).first().role.title
            auth = TokenGenerate().generate(user)
            return CustomResponse(
                general_message="successfully login",
                response=[auth, {
                    "role": user_role_title
                }],
            ).get_success_response()
        else:
            return CustomResponse(
                general_message="login failed"
            ).get_failure_response()
