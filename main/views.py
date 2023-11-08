# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import CustomUser, Author
from .serializers import CustomUserSerializer, CustomUserListSerializer, AuthorSerializer, AuthorListSerializer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password


class CurrentUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            serializer = CustomUserListSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class CustomUserView(APIView):
    permission_classes = [AllowAny]

    def to_retrieve(self, request=None, username=None):
        if username:
            user = self.get_object(username)
        else:
            user = self.get_object(request.data.get('username'))

        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return user

    def required_fields(self, request):
        if not request.data.get("first_name"):
            return Response({"detail": "First Name field is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("email"):
            return Response({"detail": "Email field is required"}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None

    def get(self, request, username=None):
        if username:
            user = self.get_object(username)
            if user is None:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomUserListSerializer(
                user)
        else:
            users = CustomUser.objects.filter(is_active=True)
            serializer = CustomUserListSerializer(
                users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        self.required_fields(request)
        request.data['password'] = make_password(request.data['password'])

        serializer = CustomUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, username=None):
        user = self.to_retrieve(request, username)
        if request.user != user and not request.user.is_staff:
            return Response({"detail": "You do not have permission to edit this user"}, status=status.HTTP_403_FORBIDDEN)

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

    def delete(self, request, username=None):
        user = self.to_retrieve(request, username)
        if request.user != user and not request.user.is_staff:
            return Response({"detail": "You do not have permission to delete this user"}, status=status.HTTP_403_FORBIDDEN)
        user.is_active = False
        user.save()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CustomUserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'detail': 'Logged in successfully'})
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)   # Isso encerrará a sessão do usuário
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)


class AuthorView(APIView):
    permission_classes = [AllowAny]

    def is_allowed(self, request):
        if not request.user.is_staff:
            return Response({"detail": "You do not have the necessary permissions"}, status=status.HTTP_403_FORBIDDEN)

    def to_retrieve(self, request=None, id=None):
        if id:
            author = self.get_object(id)
        else:
            author = self.get_object(request.data.get('id'))

        if not author:
            return Response({"detail": "Publisher not found"}, status=status.HTTP_404_NOT_FOUND)
        return author

    def get_object(self, id):
        try:
            return Author.objects.get(id=id)
        except Author.DoesNotExist:
            return None

    def get(self, request, id=None):
        if id:
            user = self.get_object(id)
            if user is None:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = AuthorListSerializer(user)
        else:
            user = Author.objects.all()
            serializer = AuthorListSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, id=None):
        self.is_allowed()
        author = self.to_retrieve(request, id)

        serializer = AuthorSerializer(
            author, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        self.is_allowed()
        author = self.to_retrieve(request, id)

        author.delete()
        return Response({"detail": "Author deleted and set as inactive"}, status=status.HTTP_200_OK)
