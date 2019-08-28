from django.contrib import admin
from .models import UserProfileInfo,Settings, Plans, Age,UpdateBaseModel,Type
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Settings)
admin.site.register(Plans)
admin.site.register(Age)
admin.site.register(UpdateBaseModel)
admin.site.register(Type)
