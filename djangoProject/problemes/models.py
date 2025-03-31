from django.db import models
from utilisateurs.models import Utilisateur

class Probleme(models.Model):
    id_utilisateur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='problemes'
    )
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    est_anonyme = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

    class Meta:
        db_table = 'problemes'
