from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver

TAGS = (
    (0,"Department"),
    (1,"Clubs"),
    (2,"placements"),
    (3,"fests"),
    (4,"hostel"),
    (5,"general")
)

TAGS = (
    (0,"Department"),
    (1,"Clubs"),
    (2,"placements"),
    (3,"fests"),
    (4,"hostel"),
    (5,"general")
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tags = MultiSelectField(choices=TAGS, default=0)
    visit = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()