from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import customers,Orders
from datetime import datetime


@receiver(post_save, sender=customers)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        full_name = f"{instance.firstname} {instance.lastname}"
        subject = 'Registration Successful'
        message = f"Dear {full_name},\n\nThank you for registering!\n\nBest regards,\nYour Foodie Team"
        from_email = 'settings.EMAIL_HOST_USER'
        to_email = instance.email
        send_mail(subject, message, from_email, [to_email])


# @receiver(pre_save, sender=Orders)
# def update_timestamp(sender, instance, **kwargs):
#     current_datetime = datetime.now()
#     datetime_now = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     instance.order_time=datetime_now
