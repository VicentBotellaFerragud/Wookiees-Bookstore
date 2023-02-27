from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.redirect_to_api_overview),
    path('overview', views.api_overview, name='overview'),
    path('books',
         views.BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list'),
    path('books/<int:pk>', views.BookViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book-detail'),
]
