from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preferred_city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.preferred_city}"