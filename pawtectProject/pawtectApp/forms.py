from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')


class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('portfolio_site','city')


class ContactForm(forms.Form):
    Full_Name = forms.CharField(required=True)
    Email = forms.EmailField(required=True)
    Mobile_Number = forms.CharField(required=True)
    Message = forms.CharField(widget=forms.Textarea, required=False)