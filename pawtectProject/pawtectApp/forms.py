from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password')


class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('portfolio_site','city')


class ContactForm(forms.Form):
    Full_Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name'}),required=True)
    Email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}),required=True)
    Mobile_Number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}),required=True)
    Message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}), required=False)