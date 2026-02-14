from django.db import models

class Livre(models.Model):
    titre = models.CharField(max_length=100)
    auteur = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)

    def __str__(self):
        return self.titre

class Emprunt(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    dateEmprunt = models.DateField()
    dateRetour = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.livre.titre} - {self.dateEmprunt}"
