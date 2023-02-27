from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login),
    path('signup/', views.CustomSignupView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login')
]
