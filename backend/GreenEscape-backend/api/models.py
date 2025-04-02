from djongo import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Utilise un hachage pour les mots de passe en production
    name = models.CharField(max_length=255, blank=True)
    games_played = models.IntegerField(default=0)  # Par exemple, pour stocker le nombre de parties jouées

    def __str__(self):
        return self.username
