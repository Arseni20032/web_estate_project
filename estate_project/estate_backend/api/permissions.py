from datetime import date

from rest_framework.permissions import BasePermission


class IsAdult(BasePermission):
    def has_permission(self, request, view):
        user_age = (date.today() - request.user.date_of_birth).days // 365
        return user_age > 18

    def has_object_permission(self, request, view, obj):
        user_age = (date.today() - request.user.date_of_birth).days // 365
        return user_age > 18


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.employee is not None

