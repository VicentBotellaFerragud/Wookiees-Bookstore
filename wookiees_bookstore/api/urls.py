from django.urls import path, include
from rest_framework import routers
from . import views

"""
router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('',  include(router.urls))
]"""

urlpatterns = [
    path('books/',
         views.BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list'),
    path('books/<int:pk>/', views.BookViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book-detail'),
]
