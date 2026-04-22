from django.conf import settings
from django.db import models

from tickets.models import Ticket


class Review(models.Model):
    """Critique (réponse à un billet)"""

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='review',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review',
    )

    rating = models.IntegerField(choices=[(i, i) for i in range(6)])
    headline = models.CharField(max_length=128, blank=True)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=['ticket', 'user'],
                name='unique_review_per_user_and_ticket',
            ),
        ]

    def __str__(self) -> str:
        return f"Review #{self.pk} ({self.user}) -> Ticket#{self.ticket.id} ({self.rating}/5)"