from django.contrib import admin
from .models import *

admin.site.register(Auteur)
admin.site.register(Livre)
admin.site.register(Categorie)
admin.site.register(Emprunt)