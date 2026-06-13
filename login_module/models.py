from django.db import models
from django.contrib.auth.models import User

class SavedCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'city_name')

    def __str__(self):
        return f"{self.user.username} - {self.city_name}"