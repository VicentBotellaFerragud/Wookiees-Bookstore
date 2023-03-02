from django.shortcuts import render, redirect
from .models import Book
from .serializers import BookSerializer
from rest_framework import permissions, serializers
from rest_framework.viewsets import ModelViewSet


def redirect_to_api_overview(request):
    return redirect('/api/overview')


def api_overview(request):
    return render(request, 'overview.html')


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.is_superuser


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if self.request.user.is_authenticated:
            context['logged_in_user'] = self.request.user.username

        return context

    def perform_create(self, serializer):
        if self.request.user.username == 'Darth_Vader':
            raise serializers.ValidationError(
                'Sorry Darth_Vader, you cannot publish your books in this book store!')
        serializer.save(author=self.request.user)
