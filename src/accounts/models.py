from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """Utilisateur"""

    photo_profile = models.ImageField(upload_to='profile', blank=True, null=True)

    followings = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Follow',
        through_fields=('follower', 'following'),
        related_name='followers',
        blank=True,
    )

    def follow(self, other: 'User'):
        if other == self:
            raise ValidationError("On ne peut pas se suivre soi-même.")

        Follow.objects.get_or_create(
            follower=self,
            following=other,
        )

    def unfollow(self, other: 'User'):
        if other == self:
            raise ValidationError("On ne peut pas se désabonner de soi-même.")

        Follow.objects.filter(
            follower=self,
            following=other,
        ).delete()

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """Relation follower -> following"""

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following_relations',
    )

    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower_relations',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow',
            ),
        ]

    def __str__(self) -> str:
        return f"{self.follower} -> {self.following}"