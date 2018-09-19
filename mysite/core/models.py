from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #bio = models.TextField(max_length=500, blank=True)
    #location = models.CharField(max_length=30, blank=True)
    #birth_date = models.DateField(null=True, blank=True)
    first_name=models.TextField(max_length=100,blank=True)
    second_name=models.TextField(max_length=100,blank=True)
    email=models.EmailField(max_length=60,blank=True)
    uid = models.UUIDField(default=uuid.uuid4)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
