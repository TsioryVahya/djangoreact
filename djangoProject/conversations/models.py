from django.db import models
from utilisateurs.models import Utilisateur

class Conversation(models.Model):
    id_participant1 = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='conversations_initiees'
    )
    id_participant2 = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='conversations_recues'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation entre {self.id_participant1.nom_utilisateur} et {self.id_participant2.nom_utilisateur}"

    class Meta:
        db_table = 'conversations'
        unique_together = ('id_participant1', 'id_participant2')  # Évite les doublons de conversations