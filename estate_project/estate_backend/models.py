from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


# class User(models.Model):
#     full_name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.full_name

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True)
    timezone = models.CharField(max_length=50, default='UTC')

    def __str__(self):
        return self.username


class Buyer(models.Model):
    phone_number_regex = RegexValidator(regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, validators=[phone_number_regex])
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class EstateType(models.Model):
    type_estate = models.CharField(max_length=255)

    def __str__(self):
        return self.type_estate


class Owner(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Employee(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    deal_count = models.IntegerField()

    def __str__(self):
        return self.full_name


class Estate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now_add=True)
    square = models.FloatField()
    number_rooms = models.IntegerField()
    ceiling_height = models.FloatField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    buyer = models.ManyToManyField(Buyer)
    responsible_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    estate_type = models.ForeignKey(EstateType, on_delete=models.CASCADE)
    cost = models.FloatField(null=True)
#    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)


class Deal(models.Model):
    estate = models.OneToOneField(Estate, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cost = models.FloatField()
    deal_date = models.DateField(auto_now_add=True)
    deal_date_end = models.DateTimeField(auto_now_add=True)
