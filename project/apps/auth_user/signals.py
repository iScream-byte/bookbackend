from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def set_user_id(sender, instance, *args, **kwargs):
    with transaction.atomic():
        if kwargs.get("created"):
            instance.user_id = f"U{str(int(instance.id)).zfill(10)}"
            instance.save()


@receiver(post_save, sender=User)
def set_token_for_user(sender, instance, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
