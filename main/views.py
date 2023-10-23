# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import CustomUser, Author
from .serializers import CustomUserSerializer, CustomUserListSerializer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password


class CustomUserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        password = serializer.validated_data.get(
            'password')  # Obtenha a senha do serializer
        user = serializer.save()
        user.set_password(password)  # Configure a senha com criptografia
        user.save()
        login(self.request, user)
        return Response(CustomUserSerializer(user).data, status=status.HTTP_201_CREATED)


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
    # Garante que o usuário esteja autenticado
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)   # Isso encerrará a sessão do usuário
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)


class CustomUserEdit(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]

    def get_object(self, username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None

    def get(self, request, username):
        user = self.get_object(username)

        if user is None:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user or request.user.is_staff:
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You do not have permission to view this user"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, username):
        user = self.get_object(username)

        if user is None:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user or request.user.is_staff:
            # Verifique se a senha foi fornecida na solicitação
            if 'password' in request.data:
                request.data['password'] = make_password(
                    request.data['password'])  # Converta a nova senha em um hash

            serializer = CustomUserSerializer(
                user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You do not have permission to edit this user"}, status=status.HTTP_403_FORBIDDEN)
# class CustomUserCreateView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer


class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer
