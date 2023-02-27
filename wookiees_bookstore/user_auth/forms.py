from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class NewUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2',)

    def save(self):
        super(NewUserForm, self).save()
