from django.db import models
from django.utils import timezone
from utilisateurs.models import User
from replies.models import Reply

class ReplyLike(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reply_likes'
        unique_together = ('reply', 'user')

    def __str__(self):
        return f"Like de {self.user.username} sur une réponse"