from rest_framework import serializers
from .models import CustomUser, Author




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['is_staff',
                   'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined', 'is_active']

class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name',
                  'profile_picture', 'sex', 'gender', 'bio', 'created_at', 'updated_at']

    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ['approved', 'updated_at']

