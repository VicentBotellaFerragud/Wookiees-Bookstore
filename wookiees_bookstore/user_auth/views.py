from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserForm


def redirect_to_login(request):
    return redirect('/login')


def log_in(request):
    return render(request, 'login.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request=self.request,
                            username=username, password=password)
        if user is not None:
            login(self.request, user)
            token, created = Token.objects.get_or_create(user=user)
            return redirect('/api' + f'?token={token.key}')
        else:
            return super().form_invalid(form)

    def form_invalid(self, form):
        print(f'Invalid form data: {form.errors}')
        return super().form_invalid(form)


class CustomSignupView(FormView):
    form_class = NewUserForm
    template_name = 'signup.html'

    def form_valid(self, form):
        form.save()
        return redirect('/login')


class SignupView(generics.CreateAPIView):
    template_name = 'signup.html'
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            return redirect('/login')

        return response
