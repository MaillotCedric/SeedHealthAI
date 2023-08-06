from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from .models import Image

class UsersListeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active"]

class UsersDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ImagesListeSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
