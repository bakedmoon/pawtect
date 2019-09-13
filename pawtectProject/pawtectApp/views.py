from __future__ import unicode_literals
from django.shortcuts import render,redirect,get_object_or_404
from .forms import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse,HttpRequest
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import threading,json
from django.contrib import messages,auth
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from .models import Settings,UserProfile,Plans,Age,Type,Pet,Coverage_Amount,Questions,PetQuestion
from .controller.UserController import UserController
from .controller.PetsController import PetsController
from pawtectProject import settings
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
    mob_otp = '123456'
    if request.method == 'POST':
        ctrl = UserController()
        num1 = str(request.POST['num1'])
        num2 = str(request.POST['num2'])
        num3 = str(request.POST['num3'])
        num4 = str(request.POST['num4'])
        num5 = str(request.POST['num5'])
        num6 = str(request.POST['num6'])
        mobile = request.POST['mobile']
        otp = num1+num2+num3+num4+num5+num6
        user = User.objects.get(username=mobile)
       
        if mob_otp == otp:
            user.is_active = True
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            auth.logout(request)
            auth.login(request,user)
            user.save()

        else:
            return HttpResponse("Something went wrong. Please try again.")
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
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

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
    types = Type.objects.all().order_by('id')
    age_group = Age.objects.all().order_by('id')

    # Set for get parmeter which we want search in model
    query_filter = utils.get_filter_params(request.GET,{},['pawtect-quote','age','name'])
    
    # Take type for fiter search result with types.(RED,YELLOW,BLUE)
    for t in types:
        plans = Plans.objects.filter(**query_filter,type_id=t.id)
        type_dict[t.name] = {'type':t,'plans':plans}
    name = request.GET.get('name','')
    age_Period = request.GET.get('age','')
    coverage_amount = request.GET.get('coverage_amount__amount','')

    return render(request,'pawtectApp/quotation.html',{"types":type_dict.items,"name":name,"age_Period":age_Period,"coverage_amount":coverage_amount})
    
def ter_of_use(request):
    return render(request,'pawtectApp/terms.html')

def pawtect_terms(request):
    return render(request,'pawtectApp/pawtect-terms.html')

def privacy_policy(request):
    return render(request,'pawtectApp/privacy.html')


# User Profile Update

def user_profile(request):

    if request.method == "GET":
        return render(request,'pawtectApp/user-profile.html',{})

    elif request.method == "POST":
        ctrl = UserController()
        myfile = request.user.userprofile.avatar
        uploadImage = False
        if request.FILES:
            myfile = request.FILES["avatar"]
            uploadImage = True

        user_profile = ctrl.userProfile(request.POST,request.user.id,myfile,uploadImage)
        return HttpResponseRedirect(reverse("my-pets"))


# Show All Pets 
def my_pets(request): 
    user_profile = request.user.userprofile
    pets = Pet.objects.filter(user_profile=user_profile).order_by('id')
    return render(request,"pawtectApp/my-pets.html",{"pets":pets})


# Create New Pet
def my_pets_new(request):
    myfile = ''
    user_profile = request.user.userprofile
    if request.method == "GET":
        return render(request,"pawtectApp/pet-profile.html",{})
    elif request.method == "POST":
        ctrl = PetsController()
        if request.FILES:
            myfile = request.FILES["picture"]
        create_pet = ctrl.create_pet(request.POST,user_profile,myfile)
        return HttpResponseRedirect(reverse("my-pets"))
    return render(request,"pawtectApp/pet-profile.html",{})


# Update/Edit Exist Pet

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
def my_pets_delete(request,petId):
    try:
        if petId:
            pet = Pet.objects.get(id=petId)
            pet.delete()
            return HttpResponseRedirect(reverse('my_proposal'))
    except Pet.DoesNotExist as e:
        return HttpResponseRedirect(reverse('my_proposal'))



def my_vetcoins(request):
    return render(request,'pawtectApp/my-vetcoins.html')

def page_not_found(request):
    return render(request,'pawtectApp/404.html')


# Get All Proposal
def my_proposal(request):
    user_profile = request.user.userprofile
    pets = Pet.objects.filter(user_profile=user_profile).order_by('id')
    questions = Questions.objects.all().order_by('id')
    # petQues = PetQuestion.objects.all()
    return render(request,"pawtectApp/my-proposal.html",{"pets":pets,"questions":questions})


# Get breed json and age model for show quotation
@csrf_exempt
def get_filter_quote_data(request):
        if request.method == 'GET':
            breed = utils.default_data()
            age_group = Age.objects.values()
            amounts = Coverage_Amount.objects.values()
            list_result = [entry for entry in age_group]
            return JsonResponse({"breed":breed,"ages":list_result,"amounts":list(amounts)})
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

# Save answers of health questions
@csrf_exempt
def saveAnswer(request):
    if request.method == "POST":
        try:
            que_obj = PetQuestion.objects.get(Q(pet_id=request.POST['pet']) & Q(questions_id=request.POST['question']))
            print("THE TRY BLOCK IS-->>",que_obj.answer)
            que_obj.answer = request.POST['answer']
            que_obj.save()
            return HttpResponse("Success")
        except PetQuestion.DoesNotExist:
            new_values = {'pet_id':request.POST['pet'],'questions_id':request.POST['question'],'answer':request.POST['answer']}
            que_obj = PetQuestion(**new_values)
            que_obj.save()
            return HttpResponse("Success")
