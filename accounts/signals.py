from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profiles

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwargs):
    if created:
        Profiles.objects.create(user=instance)