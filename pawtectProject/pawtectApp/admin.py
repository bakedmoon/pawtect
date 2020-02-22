from django.contrib import admin
from .models import UserProfile,Settings, Plans, Age,Type,Pet,Coverage_Amount,Questions,PetQuestion,\
    SalesforceSettings,SalesforceLogs
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Settings)
admin.site.register(Plans)
admin.site.register(Age)
admin.site.register(Pet)
admin.site.register(Type)
admin.site.register(Coverage_Amount)
admin.site.register(Questions)
admin.site.register(PetQuestion)
admin.site.register(SalesforceSettings)
admin.site.register(SalesforceLogs)
