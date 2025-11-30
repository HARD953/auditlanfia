from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
 
class IsLanfia(BasePermission):
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs  Superadministrateurs authentifiés
        return bool(request.user.is_agent or request.user.is_recenseur or request.user.is_lanfia)

class IsEntreprise(BasePermission):
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_entreprise  and request.user.is_active)

class IsAgentRecenseur(BasePermission):
    def has_permission(self, request, view):
    # Ne donnons l’accès qu’aux utilisateurs administrateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_recenseur and request.user.is_active)