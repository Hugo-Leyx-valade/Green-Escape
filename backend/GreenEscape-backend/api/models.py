from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    played_game = models.IntegerField(default=0)
    medails = models.IntegerField(default=0)
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


class PlayerTimePerSeed(models.Model):
    player_id = models.CharField(max_length=100)
    seed = models.CharField(max_length=100)
    time_played = models.FloatField()
    date_played = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('player_id', 'seed')

    def __str__(self):
        return f"Player {self.player_id} - Seed {self.seed}"
    


class seedStockage(models.Model):
    seed = models.IntegerField(primary_key=True, editable=False, unique=True)
    def __str__(self):
        return f"Seed {self.seed}"