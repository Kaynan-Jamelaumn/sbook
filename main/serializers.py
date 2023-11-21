from rest_framework import serializers
from .models import CustomUser, Author


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['is_staff', 'groups', 'user_permissions',
                   'last_login', 'date_joined', 'is_active']


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name',
                  'profile_picture', 'sex', 'gender', 'bio', 'birth_date', 'created_at', 'updated_at', 'password']


class CurrentCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'pseudo_name',
        fields = '__all__'
        # 'profile_picture', 'sex', 'gender', 'bio', 'birth_date', 'created_at', 'updated_at',]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ['updated_at']
