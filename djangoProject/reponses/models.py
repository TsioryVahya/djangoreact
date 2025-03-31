from django.db import models
from utilisateurs.models import Utilisateur
from problemes.models import Probleme

class Reponse(models.Model):
    id_probleme = models.ForeignKey(Probleme, on_delete=models.CASCADE, related_name='reponses')
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='reponses')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Réponse de {self.id_utilisateur} au problème {self.id_probleme}"

    class Meta:
        db_table = 'reponses'