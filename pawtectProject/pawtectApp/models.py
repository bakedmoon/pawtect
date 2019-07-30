from django.db import models
from django.contrib.auth.models import User

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio_site = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
         return self.user.username