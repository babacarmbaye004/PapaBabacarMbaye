from django.contrib import admin
from .models import Livre, Emprunt

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'isbn')
    search_fields = ('titre', 'auteur')

@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('livre', 'dateEmprunt', 'dateRetour')
    list_filter = ('dateEmprunt', 'dateRetour')
