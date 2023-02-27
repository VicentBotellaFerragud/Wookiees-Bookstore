from django.db import models
from django.conf import settings


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='covers/')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
