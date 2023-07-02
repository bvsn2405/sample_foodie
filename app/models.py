from django.db import models
from django.utils import timezone


# Create your models here.
class customers(models.Model):
    username = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,unique=True)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.username} - {self.email}"


class Orders(models.Model):
    username = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255, unique=True)
    order_time = models.DateTimeField(auto_now_add=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255, default=None)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order_id


class Payment(models.Model):
    card_number = models.CharField(max_length=100)
    cardholder = models.CharField(max_length=255)
    expirydate = models.CharField(max_length=100)
    cvv = models.CharField(max_length=100)


class PasswordResetRequest(models.Model):
    user = models.ForeignKey('app.customers', on_delete=models.CASCADE)
    email=models.CharField(max_length=100,default=None)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Password Reset Request for {self.user.email}"