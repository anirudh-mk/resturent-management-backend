import uuid

from rest_framework import serializers

from db.models import User


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
        validated_data['role'] = 'restaurant'
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('Passwords do not match')
        return data
