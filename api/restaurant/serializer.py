import uuid

from rest_framework import serializers

from db.models import User, UserRoleLink


class RestaurantCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "confirm_password",
        ]

    def create(self, validated_data):
        validated_data['id'] = uuid.uuid4()
        validated_data['username'] = validated_data['email']
        validated_data.pop('confirm_password')

        user = User.objects.create_user(**validated_data)

        UserRoleLink.objects.create(
            id=uuid.uuid4(),
            role_id=self.context.get("role_id"),
            user=user
        )

        return user

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('Passwords do not match')
        return data
