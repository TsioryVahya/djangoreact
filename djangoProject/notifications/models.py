from django.db import models
from utilisateurs.models import Utilisateur

class Notification(models.Model):
    id_utilisateur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.id_utilisateur.nom_utilisateur}: {self.message[:50]}..."

    class Meta:
        db_table = 'notifications'