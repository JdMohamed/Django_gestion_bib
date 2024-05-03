from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    bio = models.TextField()


    def __str__(self):
        return self.nom


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteurs = models.ManyToManyField(Auteur)
    categories = models.ManyToManyField(Categorie)
    isbn = models.CharField(max_length=13)
    synopsis = models.TextField()

    # Ajoutez d'autres champs comme la date de publication, le résumé, etc.

    def __str__(self):
        return self.titre


class Emprunt(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    livre = models.ForeignKey('Livre', on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(null=True, blank=True)
