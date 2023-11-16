# views.py

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

    def get(self, request, pk=None):
        return super().get(request, pk)

    # def get(self, request, id=None):
    #     if id:
    #         user = self.get_object(id)
    #         if user is None:
    #             return Response({"detail": None}, status=status.HTTP_404_NOT_FOUND)
    #         serializer = CustomUserListSerializer(
    #             user)
    #     else:
    #         users = CustomUser.objects.filter(is_active=True)
    #         serializer = CustomUserListSerializer(
    #             users, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        self.required_fields(request)
        request.data['password'] = make_password(request.data['password'])

        serializer = CustomUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, id=None):
        user = self.to_retrieve(request, id)
        if request.user != user and not request.user.is_staff:
            return Response({"error": "You do not have permission to edit this user"}, status=status.HTTP_403_FORBIDDEN)

        if 'password' in request.data:
            request.data['password'] = make_password(
                request.data['password'])  # Converta a nova senha em um hash

        serializer = CustomUserSerializer(
            user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        login(self.request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        user = self.to_retrieve(request, id)
        if request.user != user and not request.user.is_staff:
            return Response({"error": "You do not have permission to delete this user"}, status=status.HTTP_403_FORBIDDEN)
        user.is_active = False
        user.save()
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
