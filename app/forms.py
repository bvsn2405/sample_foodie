from django import forms
from app.models import customers,Order,Payment,PasswordResetRequest
import random
import string
from django.core.mail import send_mail
from django.conf import settings


def generate_otp(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def send_otp_email(email, otp):
    subject = 'Password Reset OTP'
    message = f'Your OTP for password reset is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_password_reset_email(user):
    otp = generate_otp()
    request = PasswordResetRequest(user=user, otp=otp,email=user.email)
    request.save()
    send_otp_email(user.email, otp)


