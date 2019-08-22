from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.IntegerField(blank=True, null=True)

    def __str__(self):
         return self.user.username

class UpdateBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)


class Settings(models.Model):
    key = models.CharField(max_length=100,unique=True)
    value = JSONField(blank=True, null=True)
   

class Age(models.Model):
    age_range = models.CharField(max_length=50,blank=True, null=True)
    start_age = models.CharField(max_length=50,default=0)
    end_age = models.CharField(max_length=50,default=0)

    DAYS = 'D'
    WEEKS = 'W'
    MONTHS = 'M'
    YEARS = 'Y'
    AGE_UNIT_CHOICES = [
        (DAYS, 'Days'),
        (WEEKS, 'Weeks'),
        (MONTHS, 'Months'),
        (YEARS, 'Years'),
    ]

    start_age_unit = models.CharField(max_length=50, choices=AGE_UNIT_CHOICES)
    end_age_unit = models.CharField(max_length=50, choices=AGE_UNIT_CHOICES)

    def __str__(self):
        return self.age_range

class Type(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)
    icon = models.CharField(max_length=50,blank=True, null=True)
    features = JSONField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Plans(UpdateBaseModel):
    category = models.CharField(max_length=100, blank=True, null=True)
    type = models.ForeignKey(Type, blank=True, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True, null=True)
    features = JSONField(blank=True, null=True)
    amount = models.IntegerField(default=0)
    age = models.ManyToManyField(Age)

    def __str__(self):
        return self.category