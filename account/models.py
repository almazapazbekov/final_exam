from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


user = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    register = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)




