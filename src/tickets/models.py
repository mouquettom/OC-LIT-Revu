from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


class Ticket(models.Model):
    """ Billet [demande de critique] """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
    )

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='tickets', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"Ticket #{self.pk} - {self.title}"


@receiver(pre_save, sender=Ticket)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Ticket.objects.get(pk=instance.pk)
    except Ticket.DoesNotExist:
        return

    old_image = old_instance.image
    new_image = instance.image

    if old_image and old_image != new_image:
        old_image.delete(save=False)


@receiver(post_delete, sender=Ticket)
def delete_ticket_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)