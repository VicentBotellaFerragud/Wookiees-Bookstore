from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListCreateAPIView
from .models import Book
from .serializers import BookSerializer
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer
from .models import Book
from rest_framework import serializers
from rest_framework.permissions import BasePermission


"""
def api_overview(request):
    token = request.GET.get('token')

    return render(request, 'overview.html', {'token': token})
"""


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to POST and DELETE books.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to authenticated users.
        return request.user.is_authenticated


class IsAuthorOrSuperuser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrSuperuser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context['logged_in_user'] = self.request.user.username
        return context

    def perform_create(self, serializer):
        if self.request.user.username == "Darth Vader":
            raise serializers.ValidationError(
                "You are not allowed to create books")
        serializer.save(author=self.request.user)

    """def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied(
                "You don't have permission to delete this book.")"""
