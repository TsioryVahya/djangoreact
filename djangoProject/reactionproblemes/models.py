from django.db import models
from problemes.models import Probleme
from utilisateurs.models import Utilisateur

class ReactionProbleme(models.Model):
    id_probleme = models.ForeignKey(Probleme, on_delete=models.CASCADE, related_name='reactions')
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='reactions_problemes')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reactionproblemes'
        unique_together = ('id_probleme', 'id_utilisateur')

    def __str__(self):
        return f"Réaction de {self.id_utilisateur} au problème {self.id_probleme}"
