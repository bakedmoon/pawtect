from django.contrib import admin
from .models import UserProfileInfo, User,Settings
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Settings)
