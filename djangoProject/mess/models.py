from django.db import models
from utilisateurs.models import Utilisateur
from conversations.models import Conversation

class Mess(models.Model):
    id_conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    id_expediteur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='messages_envoyes'
    )
    contenu = models.TextField()
    horodatage = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.id_expediteur.nom_utilisateur} dans conversation {self.id_conversation.id}"

    class Meta:
        db_table = 'mess'  # Nom de table spécifié selon votre schéma