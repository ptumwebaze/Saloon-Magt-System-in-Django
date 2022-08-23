# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime
from django.forms import ModelForm, Textarea
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver


# Create your models here.

class user_reg(models.Model):
    cprofile = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    nin = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=100)    
    nok = models.CharField(max_length=100)
    nokc = models.CharField(max_length=100)
    passw = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.OneToOneField(
           User, related_name="userprofile",
           on_delete=models.CASCADE, 
           null=True, blank=True
    )
    profile = models.FileField(max_length=100)    
    contact = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    otheradd = models.CharField(max_length=100)
    about = models.CharField(max_length=100)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()    


class service(models.Model):
    name = models.CharField(max_length=100)
    selling_price = models.IntegerField(default=0)
    commission = models.IntegerField(default=0)
    cost_price = models.IntegerField(default=0)
    addedby = models.CharField(default=0, max_length=100)
    status = models.CharField(default=1, max_length=1)
    addedon = models.DateTimeField(auto_now=True)

class expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    description = models.CharField(default=0, max_length=1000)
    addedby = models.CharField(default=0, max_length=100)
    status = models.CharField(default=1, max_length=1)
    addedon = models.DateTimeField(auto_now=True)

class employee(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    commission = models.IntegerField(default=0, max_length=10)
    paid = models.IntegerField(default=0, max_length=10)
    balance = models.IntegerField(default=0, max_length=10)
    addedby = models.CharField(default=0, max_length=100)
    status = models.CharField(default=1, max_length=1)
    addedon = models.DateTimeField(auto_now=True)
    


class order(models.Model):
    customer = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=100)
    amount = models.IntegerField(default=0, max_length=100)
    paid = models.IntegerField(default=0, max_length=100)
    balance = models.IntegerField(default=0, max_length=100)
    mode = models.CharField(max_length=100)
    added_by = models.CharField(max_length=100)
    status = models.IntegerField(default=0, max_length=1)
    added_on = models.DateTimeField(auto_now=True)

class orderdetail(models.Model):
    staff = models.CharField(default=0, max_length=100)
    service = models.CharField(max_length=100)
    service_price = models.IntegerField(default=0, max_length=100)
    order_id = models.IntegerField(default=0, max_length=100)
    added_by = models.CharField(max_length=100)
    status = models.IntegerField(default=0, max_length=1)
    added_on = models.DateTimeField(auto_now=True)

class cart(models.Model):
    service = models.CharField(max_length=100)
    service_price = models.IntegerField(default=0)
    staff = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    added_by = models.CharField(default=0, max_length=100)
    added_on = models.DateTimeField(auto_now=True)

    # @property
    # def price(self):
    #     return sum(int(self.total)).aggregate


class logs(models.Model):
    activity = models.CharField(max_length=100)
    user = models.CharField(default=0, max_length=100, null=True, blank=True)
    added_on = models.DateTimeField(auto_now=True)

