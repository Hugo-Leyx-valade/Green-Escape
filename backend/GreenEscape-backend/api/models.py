from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    played_game = models.IntegerField(default=0)
    win = models.IntegerField(default=0)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Évite le conflit
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Évite le conflit
        blank=True
    )

    def __str__(self):
        return self.username