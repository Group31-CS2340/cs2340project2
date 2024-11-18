from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from django.utils.translation import gettext_lazy as _

def register_user(username, first_name, last_name, email, password):
    if not email:
        raise ValueError("Email field is required")
    if not password:
        raise ValueError("Password field is required")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wraps = models.ManyToManyField('Wrap', blank=True)
    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Feedback(models.Model):
    message = models.TextField()             
    submitted_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Feedback submitted on {self.submitted_at}"

class Wrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    top_artists = models.JSONField(default=list)
    top_tracks = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

