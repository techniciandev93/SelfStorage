from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from selfstorage.settings import EMAIL_HOST_USER
from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать!'
        message = f'Спасибо за регистрацию {instance.email}. Мы рады видеть вас здесь!'
        send_mail(subject, message, EMAIL_HOST_USER, [instance.email])
