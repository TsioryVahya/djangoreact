from django.db import models
from django.utils import timezone
from utilisateurs.models import User
from conversations.models import Conversation

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"Message de {self.sender.username} dans {self.conversation}"