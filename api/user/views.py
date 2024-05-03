from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.user.serializer import UserCreateSerializer
from db.models import Role
from utils.response import CustomResponse


class CreateUserAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        role_id = Role.objects.filter(title='USER').first().id

        serializer = UserCreateSerializer(
            data=request.data,
            context={
                "role_id": role_id
            }
        )
        if serializer.is_valid():
            serializer.save()

            return CustomResponse(
                general_message='User created successfully'
            ).get_success_response()

        return CustomResponse(
            response=serializer.errors
        ).get_failure_response()
