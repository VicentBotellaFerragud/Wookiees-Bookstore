from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import NewUserForm
from .utils import authenticate_and_log_in_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def redirect_to_login(request):
    return redirect('/login')


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/api')
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate_and_log_in_user(self.request, form)
        token, created = Token.objects.get_or_create(user=user)

        return redirect('/api' + f'?token={token.key}')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'invalid_credentials': form})


class CustomSignupView(FormView):
    form_class = NewUserForm
    template_name = 'signup.html'

    def form_valid(self, form):
        form.save()
        user = authenticate_and_log_in_user(self.request, form, 'signup')
        token, created = Token.objects.get_or_create(user=user)

        return redirect('/api' + f'?token={token.key}')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


@login_required(login_url='/login')
def log_out(request):
    logout(request)

    return redirect('/login')
