from django.contrib import admin
from .models import UserProfile,Settings, Plans, Age,Type,Pet
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Settings)
admin.site.register(Plans)
admin.site.register(Age)
admin.site.register(Pet)
admin.site.register(Type)
