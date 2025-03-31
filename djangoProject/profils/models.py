from django.db import models
from utilisateurs.models import Utilisateur

class Profil(models.Model):
    id_utilisateur = models.OneToOneField(
        Utilisateur, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='profil'
    )
    url_avatar = models.CharField(max_length=255, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil de {self.id_utilisateur.nom_utilisateur}"

    class Meta:
        db_table = 'profils'