from __future__ import unicode_literals
from django.shortcuts import render,redirect
from .forms import UserForm,UserProfileInfoForm,ContactForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from twilio.rest import Client
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'pawtectApp/login.html')

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
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("USERNAME IS==>>",username,password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return render(request,'pawtectApp/onboard.html')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'pawtectApp/login.html', {})



def contact(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request,'pawtectApp/contact.html',{'form': form})
    else:
        form = ContactForm(request.POST)
        print("THE REQUESTED BODY IS==>>",request.POST)
        if form.is_valid():
            name = form.cleaned_data['Full_Name']
            Mobile_Number = form.cleaned_data['Mobile_Number']
            from_email = form.cleaned_data['Email']
            message = form.cleaned_data['Message']
            subject = "Someone Contact Us!"
            try:
                send_mail(subject, message, from_email, ['Sagar Jadhav<sagar.crive@gmail.com>'])
            except BadHeaderError:
                messages.error(request,"Something went wrong try again.")
            sendMailToUser(from_email,name)
            messages.success(request,"Mail Send Successfully.")

    return render(request, "pawtectApp/contact.html", {'form': form})

def sendMailToUser(toEmail,name):
    subject = "Thanks for contact us!"
    message = "We are contact u in short time"
    fromEmail = "sagar.crive@gmail.com"
    toEmail = toEmail
    send_mail(subject, message,'', [toEmail])
    