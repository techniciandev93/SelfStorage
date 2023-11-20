from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from .models import CustomUser
from selfstorage.settings import EMAIL_HOST_USER


@shared_task
def send_notifications():
    clients_3_days = list(CustomUser.objects.filter(
        orders__end_rent_date__date=(timezone.now() + timedelta(days=3)).date(), orders__paid=True).values())
    clients_week = list(CustomUser.objects.filter(
        orders__end_rent_date__date=(timezone.now() + timedelta(days=7)).date(), orders__paid=True).values())
    clients_2_weeks = list(CustomUser.objects.filter(
        orders__end_rent_date__date=(timezone.now() + timedelta(days=14)).date(), orders__paid=True).values())
    send_mail_for_group.delay(clients_2_weeks, 'Ваша аренда заканчивается через 2 недели')
    send_mail_for_group.delay(clients_week, 'Ваша аренда заканчивается через неделю')
    send_mail_for_group.delay(clients_3_days, 'Ваша аренда заканчивается через 3 дня')


@shared_task
def send_mail_for_group(users, message):
    subject = 'Уведомление о скором окончании срока аренды'
    sender = EMAIL_HOST_USER
    emails = [user['email'] for user in users]
    send_mail(
        subject=subject,
        message=message,
        from_email=sender,
        recipient_list=emails
    )
    return emails
