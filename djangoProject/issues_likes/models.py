from django.db import models
from django.utils import timezone
from utilisateurs.models import User
from issues.models import Issue

class IssueLike(models.Model):
    issues = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'issues_likes'
        unique_together = ('issues', 'user')

    def __str__(self):
        return f"Like de {self.user.username} sur {self.issues.title}"