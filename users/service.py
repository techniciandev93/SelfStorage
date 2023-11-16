from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_email(sender, instance, created, **kwargs):
    if created:
        print('Зареган', instance.email)
        #send_mail(subject, message, from_email, [to_email])
