from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('signup', views.CustomSignupView.as_view(), name='signup'),
    path('logout', views.log_out, name='login')
]
