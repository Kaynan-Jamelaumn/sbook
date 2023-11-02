# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from .models import CustomUser, Author
from .serializers import CustomUserSerializer, CustomUserListSerializer, AuthorSerializer, AuthorListSerializer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from piece.models import Piece




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
        print(user,"aaa")
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




class AuthorCreate(generics.CreateAPIView):
    permission_classes = [IsAdminUser]

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorEdit(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, id):
        author = Author.objects.get(id=id)
        if request.user == author.user or request.user.is_staff:
            serializer = AuthorSerializer(
                author, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "You do not have permission to edit this author"}, status=status.HTTP_403_FORBIDDEN)


class AuthorUpdate(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, id):
        author = Author.objects.get(id=id)
        if request.user == author.user or request.user.is_staff:
            author.is_active = False
            author.save()
            return Response({"detail": "Author updated and set as inactive"}, status=status.HTTP_200_OK)
        return Response({"detail": "You do not have permission to update this author"}, status=status.HTTP_403_FORBIDDEN)


class AuthorDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        author = Author.objects.get(id=id)
        if request.user == author.user or request.user.is_staff:
            author.is_active = False
            author.save()
            return Response({"detail": "Author deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission to delete this author"}, status=status.HTTP_403_FORBIDDEN)


class AuthorDetail(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser]

    def get(self, request, id):
        author = Author.objects.get(id=id)
        serializer = AuthorSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorsList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorListSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


