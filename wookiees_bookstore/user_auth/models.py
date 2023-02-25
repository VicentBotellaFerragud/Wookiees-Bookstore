from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    author_pseudonym = models.CharField(max_length=30)
