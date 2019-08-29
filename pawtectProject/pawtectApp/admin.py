from django.contrib import admin
from .models import UserProfileInfo,Settings, Plans, Age,Type,Pet
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Settings)
admin.site.register(Plans)
admin.site.register(Age)
admin.site.register(Pet)
admin.site.register(Type)
