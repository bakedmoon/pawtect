from __future__ import unicode_literals
from django.shortcuts import render,redirect,get_object_or_404
from .forms import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import threading,json
from django.contrib import messages,auth
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from .models import Settings,UserProfile,Plans,Age,Type,Pet
from .controller.UserController import UserController
from .controller.PetsController import PetsController
from . import utils
from . import const

    
# Landing Page
def index(request):
    return render(request, 'pawtectApp/index.html',{})
    try:
        settings = Settings.objects.get(key='home_banner_image')
        url = settings.value['url']
        return render(request, 'pawtectApp/index.html',{'imageUrl':url})
    except Settings.DoesNotExist:
        return render(request, 'pawtectApp/index.html',{})


def home(request):
    return render(request, 'pawtectApp/home.html',{})
    try:
        settings = Settings.objects.get(key='home_banner_image')
        url = settings.value['url']
        return render(request, 'pawtectApp/home.html',{'imageUrl':url})
    except Settings.DoesNotExist:
       return render(request, 'pawtectApp/home.html',{})


# Register/Signup User
def signup(request):
    if request.method == 'POST':
        ctrl = UserController()
        if request.POST['password'] == request.POST['password2']:
            existUser = User.objects.filter(Q(email=request.POST['email']) | Q(username=request.POST['mobile'])).exists()
            if existUser:
                messages.error(request,'User already exist for email or mobile number.')
                return HttpResponseRedirect(reverse('register'))
            else:
                usersignup = ctrl.userSignup(request.POST)
                return render(request,'pawtectApp/signup.html',{'is_otpModal':True,'mobileNumber':request.POST['mobile']})
        else:
            messages.error(request,'Password not match.')
            return HttpResponseRedirect(reverse('register'))
    else:
        return render(request,'pawtectApp/signup.html',{'is_otpModal':False})


def otp(request):
    if request.method == 'POST':
        ctrl = UserController()
        num1 = request.POST['num1']
        num2 = request.POST['num2']
        num3 = request.POST['num3']
        num4 = request.POST['num4']
        num5 = request.POST['num5']
        num6 = request.POST['num6']
        mobile = request.POST['mobile']
        otp = num1+num2+num3+num4+num5+num6
        userotp=ctrl.otpVerify(otp,mobile)
        return HttpResponseRedirect(reverse('my-pets'))

    
# User Login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        
        user =auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('my-pets'))
        else:
            messages.error(request,"Something went wrong try again.")
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'pawtectApp/login.html')

# User Logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

# Contact 
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request,'pawtectApp/contact.html',{'form': form})
    else:
        form = ContactForm(request.POST)
       
        if form.is_valid():
            name = form.cleaned_data['Full_Name']
            Mobile_Number = form.cleaned_data['Mobile_Number']
            to_email = form.cleaned_data['Email']
            message = form.cleaned_data['Message']
            subject = "Someone Contact Us!"
            try:
                send_mail(subject, message, '', [const.ADMIN_MAIL])
            except BadHeaderError:
                messages.error(request,"Something went wrong try again.")
            userMail = threading.Thread(target=utils.sendMailToUser, args=(to_email,name))
            userMail.start()
            userMail.join()
            messages.success(request,"Mail Send Successfully.")
            return HttpResponseRedirect(reverse('contact'))
    return render(request, "pawtectApp/contact.html", {'form': form})
    

def plans(request):
    return render(request,'pawtectApp/plans.html')

def review(request):
    return render(request,'pawtectApp/review.html')

def aboutUs(request):
    return render(request,'pawtectApp/aboutUs.html')


# Search Quotation Details
def quotation(request):
    query_filter = {}
    type_dict = {}
    breedInfo = ''
    types = Type.objects.all()
    age_group = Age.objects.all()

    # Set for get parmeter which we want search in model
    query_filter = utils.get_filter_params(request.GET,{},['pawtect-quote'])
    
    # Take type for fiter search result with types.(RED,YELLOW,BLUE)
    for t in types:
        plans = Plans.objects.filter(**query_filter,type_id=t.id)
        type_dict[t.name] = {'type':t,'plans':plans}

    return render(request,'pawtectApp/quotation.html',{"types":type_dict.items})
    
def ter_of_use(request):
    return render(request,'pawtectApp/terms.html')

def privacy_policy(request):
    return render(request,'pawtectApp/privacy.html')


# User Profile Update
@login_required(login_url='/login/')
@csrf_exempt
def user_profile(request):
    userId = request.user.id
    user = UserProfile.objects.get(user_id=request.user.id)

    if request.method == "GET":
        return render(request,'pawtectApp/user-profile.html',{'user':user})

    elif request.method == "POST":
        ctrl = UserController()
        myfile = user.avatar
        uploadImage = False
        if request.POST['avatar']:
            myfile = "/media/"+request.POST['avatar']
            uploadImage = True
        user_profile = ctrl.userProfile(request.POST,userId,myfile,uploadImage)
        return HttpResponseRedirect(reverse("my-pets"))


# Show All Pets 
@login_required(login_url='/login/')
def my_pets(request):
    user_profile = request.user.userprofile
    pets = Pet.objects.filter(user_profile=user_profile).order_by('id')
    return render(request,"pawtectApp/my-pets.html",{"pets":pets})


# Create New Pet
@login_required(login_url='/login/')
def my_pets_new(request):
    user_profile = request.user.userprofile
    if request.method == "GET":
        return render(request,"pawtectApp/pet-profile.html",{})
    elif request.method == "POST":
        ctrl = PetsController()
        myfile = request.FILES["picture"]
        create_pet = ctrl.create_pet(request.POST,user_profile,myfile)
        return HttpResponseRedirect(reverse("my-pets"))
    return render(request,"pawtectApp/pet-profile.html",{})


# Update/Edit Exist Pet
@login_required(login_url='/login/')
def my_pets_edit(request,petId):
    if request.method == "GET":
       pet = Pet.objects.get(id=petId)
       return render(request,"pawtectApp/pet-profile.html",{"pet":pet})
    if request.method == "POST":
        user_profile = request.user.userprofile
        pet = Pet.objects.get(id=petId)
        myfile = pet.picture
        uploadImage = False
        ctrl = PetsController()
        if request.FILES:
            myfile = request.FILES["picture"]
            uploadImage = True
        update_pet = ctrl.update_pet(request.POST,user_profile,petId,myfile,uploadImage)
        return HttpResponseRedirect(reverse('my-pets'))


# Delete Exist Pet
@login_required(login_url='/login/')
def my_pets_delete(request,petId):
    try:
        if petId:
            pet = Pet.objects.get(id=petId)
            pet.delete()
            return HttpResponseRedirect(reverse('my_proposal'))
    except Pet.DoesNotExist as e:
        return HttpResponseRedirect(reverse('my_proposal'))


@login_required(login_url='/login/')
def my_vetcoins(request):
    return render(request,'pawtectApp/my-vetcoins.html')


# Get All Proposal
@login_required(login_url='/login/')
def my_proposal(request):
    user_profile = request.user.userprofile
    pets = Pet.objects.filter(user_profile=user_profile).order_by('id')
    return render(request,"pawtectApp/my-proposal.html",{"pets":pets})


# Get breed json and age model for show quotation
def get_filter_quote_data(request):
        if request.method == 'GET':

            breed = utils.default_data()
            
            age_group = Age.objects.values()
            list_result = [entry for entry in age_group]
            return JsonResponse({"breed":breed,"ages":list_result})
        else:
            return HttpResponse("Something went wrong. Please try again.")


# Single Proposal View
def my_proposal_view(request,petId):
    if petId:
        pet = Pet.objects.get(id=petId)
        return render(request,"pawtectApp/my-proposal-view.html",{'pet':pet})


# Get Country Data
def get_country_data(request):
    if request.method == 'GET':
        country = utils.default_data_country()
        return JsonResponse({"country":country})
    else:
        return HttpResponse("Something went wrong. Please try again.")