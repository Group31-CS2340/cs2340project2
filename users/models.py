from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def register_user(username, first_name, last_name, email, password):
    if not email:
        raise ValueError("Email field is required")
    if not password:
        raise ValueError("Password field is required")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_restaurants = models.TextField(blank=True)
    dietary_restrictions = models.CharField(max_length=255, blank=True)
    favorite_cuisine_types = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Review(models.Model):
    restaurant_name = models.CharField("restaurant name", max_length=150, blank=True)
    rating = models.IntegerField("rating", default=0)
    review = models.TextField("review", blank=True)