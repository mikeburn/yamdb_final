from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsAdmin(BasePermission):
    """Есть ли права администратора"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAnonymousGuest(BasePermission):
    """Анонимный пользователь"""
    def has_permission(self, request, view):
        return request.user.is_anonymous


class AdminOrReadonly(BasePermission):
    """Чтение для всех,
    изменения-только администратор"""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS) or (
            (request.user.is_authenticated and (
                (request.user.is_admin or request.user.is_staff)))
        )


class AuthorModeratorAdminOrReadOnly(BasePermission):
    """"Доступ - автор, модератор или администратор."""

    def has_permission(self, request, view):
        return (request.method
                in SAFE_METHODS) or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS) or (
            (request.user == obj.author
                or request.user.is_moderator
                or request.user.is_admin)
        )
