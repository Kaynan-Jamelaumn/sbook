
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from piece.views import BaseView

from .models import CustomUser, Author
from .serializers import CustomUserSerializer, CustomUserListSerializer, CurrentCustomUserSerializer, AuthorSerializer, AuthorListSerializer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from piece.views import BaseView


class CurrentUserView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            serializer = CurrentCustomUserSerializer(request.user)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        return Response({"user": None}, status=status.HTTP_404_NOT_FOUND)


class CustomUserView(BaseView):
    def __init__(self, model=CustomUser, param_name="id", serializer=CustomUserSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request, id=None):
        return super().get(request, id)

    def required_fields(self, request):
        if not request.data.get("first_name"):
            return "First Name field is required"
        if not request.data.get("email"):
            return "Email field is required"
        return False

    def post(self, request):
        message = self.required_fields(request)
        if message:
            return Response({"detail": "Email field is required"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['password'] = make_password(request.data['password'])

        serializer = CustomUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        login(request, user)

        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, id=None):
        user = self.to_retrieve(request, id)

        if isinstance(user, self.serializer):  # Check if user is a serializer
            user_instance = user.instance  # Extract the model instance from the serializer
        else:
            user_instance = user

        if request.user != user_instance and not request.user.is_staff:
            return Response({"error": "You do not have permission to edit this user"}, status=status.HTTP_403_FORBIDDEN)

        if 'password' in request.data:
            request.data['password'] = make_password(request.data['password'])

        serializer = self.serializer(
            user_instance, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        user = self.to_retrieve(request, id)

        if isinstance(user, self.serializer):  # Check if user is a serializer
            user_instance = user.instance  # Extract the model instance from the serializer
        else:
            user_instance = user
        if request.user != user and not request.user.is_staff:
            return Response({"error": "You do not have permission to delete this user"}, status=status.HTTP_403_FORBIDDEN)
        user_instance.is_active = False
        user_instance.save()
        return Response({"error": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CustomUserLogin(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            serializer = CurrentCustomUserSerializer(request.user)
            return Response({'user': serializer.data})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)   # Isso encerrará a sessão do usuário
        return Response({"success": True}, status=status.HTTP_200_OK)


class AuthorView(BaseView):
    def __init__(self, model=Author, param_name="id", serializer=AuthorSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request, pk=None):
        return super().get(request, pk)

    def post(self, request):
        return super().post(request)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)
