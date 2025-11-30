# api/views.py
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout, login
from .serializers import UserLoginSerializer, UserLogoutSerializer
from rest_framework import generics
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *

class DetailConecter(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        if self.request.user.is_authenticated:
            dons=CustomUser.objects.filter(email=self.request.user.email)
            serializer=UserSerializer(dons, many=True)
            return Response({'data':serializer.data,'status':status.HTTP_200_OK})
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST})

# class UserListCreateView(generics.ListCreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         # Filtrer les objets DonneeCollectee pour l'utilisateur connecté et l'entreprise associée
#         user = self.request.user
#         if user.is_agent:  # Vérifie si l'utilisateur est connecté
#             return CustomUser.objects.all()
#         else:
#             return CustomUser.objects.filter(entreprise=user.entreprise)
        
class UserListCreateViewAgent(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(is_agent=True)
    
class UserListCreateViewEntreprise(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(is_entreprise=True)

class UserListCreateViewRecenseur(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(is_recenseur=True)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class UserSerializer1(generics.ListAPIView):
    queryset = CustomUser.objects.all().values('entreprise').distinct()
    serializer_class = UserSerializer1

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def user_login(request):
#     serializer = UserLoginSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
        
#         user = authenticate(request, email=email, password=password)
        
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 token, created = Token.objects.get_or_create(user=user)
#                 return Response({'token': token.key}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'User account is disabled.'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def user_logout(request):
#     request.auth.delete()
#     logout(request)
#     return Response({'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)