from django.db import models
from reponses.models import Reponse
from utilisateurs.models import Utilisateur

class ReactionReponse(models.Model):
    id_reponse = models.ForeignKey(Reponse, on_delete=models.CASCADE, related_name='reactions')
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='reactions_reponses')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reactionreponses'
        unique_together = ('id_reponse', 'id_utilisateur')

    def __str__(self):
        return f"Réaction de {self.id_utilisateur} à la réponse {self.id_reponse}"