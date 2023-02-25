from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm


class SignupView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


def log_in(request):
    return render(request, 'login.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        print(f"form_valid called with {len(self.args)} arguments")
        author_pseudonym = form.cleaned_data['author_pseudonym']
        username = form.cleaned_data['username']
        # email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request=self.request,
                            username=username, password=password)
        if user is not None:
            login(self.request, user)
            token, created = Token.objects.get_or_create(user=user)
            return HttpResponseRedirect(reverse('home') + f'?token={token.key}')
        else:
            return super().form_invalid(form)

    def form_invalid(self, form):
        print(f'Invalid form data: {form.errors}')
        return super().form_invalid(form)


@login_required
def home(request):
    token = request.GET.get('token')
    return render(request, 'home.html', {'token': token})
