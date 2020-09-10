from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


# post save are done from user is saved, signal is sent
# will the signal is going to be received from a function (will be decorated)
# we will know if the user object who is signaling is being
# created or being modified
# within the function we're going to creating a profile instance
# and connect it to the user

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     print('created:', created)
#     if created:
#         Profile.objects.create(user=instance)
