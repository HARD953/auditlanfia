# api/urls.py

from django.urls import path
from .views import*
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('uagent/', UserListCreateViewAgent.as_view(), name='user-lista-create'),  # Liste et création d'utilisateurs
    path('uentreprise/', UserListCreateViewEntreprise.as_view(), name='user-liste-create'),  # Liste et création d'utilisateurs
    path('urecenseur/', UserListCreateViewRecenseur.as_view(), name='user-listr-create'),  # Liste et création d'utilisateurs
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Détails, mise à jour et suppression d'un utilisateur
    path('detailadimn/', DetailConecter.as_view(),name='detail-des-admin'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('entreprise/', UserSerializer1.as_view(), name='entreprise'),
    
    # ... Autres URL pour d'autres vues si nécessaire
]
