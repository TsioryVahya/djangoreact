from django.db import models
from django.utils import timezone
from utilisateurs.models import User

class Conversation(models.Model):
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conv_participant1')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conv_participant2')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'conversations'

    def __str__(self):
        return f"Conversation entre {self.participant1.username} et {self.participant2.username}"