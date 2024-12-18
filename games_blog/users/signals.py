from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
from users.tasks import send_verification_email_task


@receiver(post_save, sender=User)
def send_verif(sender, instance, created, *args, **kwargs):
    if created:
        send_verification_email_task.delay(instance.pk)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
