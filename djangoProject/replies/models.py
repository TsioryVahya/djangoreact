from django.db import models
from django.utils import timezone
from utilisateurs.models import User
from issues.models import Issue

class Reply(models.Model):
    issues = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'replies'

    def __str__(self):
        return f"Réponse de {self.user.username} à {self.issues.title}"