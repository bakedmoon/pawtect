from __future__ import unicode_literals
from django.shortcuts import render,redirect
from .forms import UserForm,UserProfileInfoForm,ContactForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'pawtectApp/index.html',{})
    try:
        settings = Settings.objects.get(key='home_banner_image')
        url = settings.value['url']
        return render(request, 'pawtectApp/index.html',{'imageUrl':url})
    except Settings.DoesNotExist:
        return render(request, 'pawtectApp/index.html',{})

def reg(request):
    return render(request, 'pawtectApp/registration.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'pawtectApp/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
def login(request):
    form = UserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            return HttpResponseRedirect(reverse('plans'))
        else:
            messages.error(request,"Something went wrong try again.")
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'pawtectApp/login.html')



def contact(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request,'pawtectApp/contact.html',{'form': form})
    else:
        form = ContactForm(request.POST)
       
        if form.is_valid():
            name = form.cleaned_data['Full_Name']
            Mobile_Number = form.cleaned_data['Mobile_Number']
            from_email = form.cleaned_data['Email']
            message = form.cleaned_data['Message']
            subject = "Someone Contact Us!"
            try:
                send_mail(subject, message, from_email, ['Sagar Jadhav<sagar@bakedmoon.studio>'])
            except BadHeaderError:
                messages.error(request,"Something went wrong try again.")
            sendMailToUser(from_email,name)
            messages.success(request,"Mail Send Successfully.")
            return HttpResponseRedirect(reverse('contact'))
    return render(request, "pawtectApp/contact.html", {'form': form})

def sendMailToUser(toEmail,name):
    subject = "Thanks for contact us!"
    message = "We are contact u in short time"
    fromEmail = "sagar.crive@gmail.com"
    toEmail = toEmail
    send_mail(subject, message,'Sagar Jadhav<sagar.crive@gmail.com>', [toEmail])
    

def plans(request):
    return render(request,'pawtectApp/plans.html')

def review(request):
    return render(request,'pawtectApp/review.html')

def aboutUs(request):
    return render(request,'pawtectApp/aboutUs.html')

def quotation(request):
    return render(request,'pawtectApp/quotation.html')

def ter_of_use(request):
    return render(request,'pawtectApp/terms.html')

def privacy_policy(request):
    return render(request,'pawtectApp/privacy.html')

