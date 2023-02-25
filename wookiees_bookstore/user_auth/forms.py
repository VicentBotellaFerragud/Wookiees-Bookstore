from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    author_pseudonym = forms.CharField(max_length=30, required=True)