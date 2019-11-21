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
from datetime import date,datetime
from django.contrib import messages,auth
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from .models import Settings,UserProfile,Plans,Age,Type,Pet,Coverage_Amount,Questions,PetQuestion,SalesforceSettings,SalesforceLogs
from .controller.UserController import UserController
from .controller.PetsController import PetsController
from .Services.SalesforceService import SalesforceService
from pawtectProject import settings
from . import utils
from . import const

today = date.today()
    
# Home Page
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
                user = User.objects.get(Q(email=request.POST['email']) | Q(username=request.POST['mobile']))
                if user.is_active:
                    messages.error(request,'User already exist for email or mobile number.')
                    return HttpResponseRedirect(reverse('register'))
                else:
                    return render(request,'pawtectApp/signup.html',{'is_otpModal':True,'mobileNumber':request.POST['mobile']})
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
            sfObj = SalesforceService()
            sfInfo = SalesforceSettings.objects.get()

            if sfInfo:
                accessData = sfObj.createNewUser(sfInfo,user.id)
                
                if accessData and  accessData[0]['isSuccess']:
                    user.is_active = True
                    user.backend = settings.AUTHENTICATION_BACKENDS[0]
                    auth.logout(request)
                    auth.login(request, user)
                    user.save()

                    return HttpResponseRedirect(reverse('my-pets'))
                else:
                    return HttpResponseRedirect(reverse('page_not_found'))

            else:
                return HttpResponseRedirect(reverse('page_not_found'))

        else:
            return HttpResponseRedirect(reverse('page_not_found'))



    
# User Login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        
        user =auth.authenticate(username=username, password=password)

        if not user:
            try:
                user = User.objects.get(email = username)
                username = user.username
                user = auth.authenticate(username=username, password=password)

            except User.DoesNotExist as e:
                messages.error(request,"")
            
        
        if user:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('my-pets'))
        else:
            messages.error(request,"User does not exist.")
            return HttpResponseRedirect(reverse('user_login'))
    else:
        return render(request, 'pawtectApp/login.html')

# User Logout
@login_required(login_url='user_login')
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))

def forgot_password(request):
    return render(request,'pawtectApp/forgot-password.html')

def reset_password(request):
    return render(request,'pawtectApp/reset-password.html')

def change_password(request):
    print("INSIDE CHANGE PASSWORD")
    if request.method == "GET":
        return render(request,'pawtectApp/change-password.html')
    elif request.method == "POST":
        print("THE REQUEST POST IS HERE--->>>",request.POST)

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
    planCount = []
    types = Type.objects.all().order_by('id')
    age_group = Age.objects.all().order_by('id')

    # Set for get parmeter which we want search in model
    query_filter = utils.get_filter_params(request.GET,{},['pawtect-quote','age','name'])
    
    # Take type for fiter search result with types.(RED,YELLOW,BLUE)
    listCount = []
    for t in types:
        plans = Plans.objects.filter(**query_filter,type_id=t.id)
        
        planNumber = plans.count()
        planCount.append(planNumber)
        listCount = sum(planCount)
        type_dict[t.name] = {'type':t,'plans':plans}
    name = request.GET.get('name','')
    age_Period = request.GET.get('age','')
    coverage_amount = request.GET.get('coverage_amount__amount','')

    return render(request,'pawtectApp/quotation.html',{"types":type_dict.items,"name":name,"age_Period":age_Period,"coverage_amount":coverage_amount,"planCount":listCount})
    
def ter_of_use(request):
    return render(request,'pawtectApp/terms.html')

def pawtect_terms(request):
    return render(request,'pawtectApp/pawtect-terms.html')

def privacy_policy(request):
    return render(request,'pawtectApp/privacy.html')


# User Profile Update
@login_required(login_url='user_login')
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
@login_required(login_url='user_login')
def my_pets(request):
    sfObj = SalesforceService()
    user_profile = request.user.userprofile
    vetcoins = sfObj.getVetcoinsDetails(user_profile)

    if vetcoins:
        pets = Pet.objects.filter(user_profile=user_profile).order_by('id')
        petsCount = pets.count()
        for petBirth in pets:
            diffrence = today - petBirth.birthDate
            actualDays = diffrence.days
            if actualDays < const.SMALL_AGE_LIMIT or actualDays > const.MAX_AGE_LIMIT:
                petBirth.disabledClass = True
            else:
                petBirth.disabledClass = False
    else:
        messages.error(request,"Something went wrong. Please try again.")
        return None

    return render(request,"pawtectApp/my-pets.html",{"pets":pets,"petsCount":petsCount})

# Create New Pet
@login_required(login_url='user_login')
def my_pets_new(request):
    myfile = ''
    microchipNumber = ''
    existChipNumber = ''
    pet = {}
    user_profile = request.user.userprofile
    if request.method == "GET":
        return render(request,"pawtectApp/pet-profile.html",{})
    elif request.method == "POST":
        if len(request.POST['microchip_Number']) > 0:
            #Check if exist or not microchip number
            ifExist = utils.checkMicrochipNumber(request.POST['microchip_Number'])

            if ifExist:
                messages.error(request,"Microchip number "+"[ "+request.POST['microchip_Number']+" ]"+" already exist.")

                #Get fill pet info using service.
                getPetInfo = utils.afterErrorPetData(request.POST)
                return render(request,"pawtectApp/pet-profile.html",{"pet":getPetInfo})
            else:
                ctrl = PetsController()
                if request.FILES:
                    myfile = request.FILES["picture"]
                create_pet = ctrl.create_pet(request.POST,user_profile,myfile)
                return HttpResponseRedirect(reverse("my-pets"))
        else:
                ctrl = PetsController()
                if request.FILES:
                    myfile = request.FILES["picture"]
                create_pet = ctrl.create_pet(request.POST,user_profile,myfile)
                return HttpResponseRedirect(reverse("my-pets"))

    return render(request,"pawtectApp/pet-profile.html",pet)


# Update/Edit Exist Pet
@login_required(login_url='user_login')
def my_pets_edit(request,petId):
    pet = Pet.objects.get(id=petId)
    if request.method == "GET":
       return render(request,"pawtectApp/pet-profile.html",{"pet":pet})

    if request.method == "POST":

        if request.POST['microchip_Number'] != pet.microchip_Number:

            #Check if exist or not microchip number
            ifExist = utils.checkMicrochipNumber(request.POST['microchip_Number'])
            
            if ifExist:
                messages.error(request,"Microchip number "+"[ "+request.POST['microchip_Number']+" ]"+" already exist.")
                
                #To stay same page call edit url again. For this send petId to url.
                url = reverse('my-pets-edit', kwargs={'petId': petId})
                return HttpResponseRedirect(url)

            else:
                user_profile = request.user.userprofile
                myfile = pet.picture
                uploadImage = False
                ctrl = PetsController()
                if request.FILES:
                    myfile = request.FILES["picture"]
                    uploadImage = True
                update_pet = ctrl.update_pet(request.POST,user_profile,petId,myfile,uploadImage)
                return HttpResponseRedirect(reverse('my-pets'))

        else:
            user_profile = request.user.userprofile
            myfile = pet.picture
            uploadImage = False
            ctrl = PetsController()
            if request.FILES:
                myfile = request.FILES["picture"]
                uploadImage = True
            update_pet = ctrl.update_pet(request.POST,user_profile,petId,myfile,uploadImage)
            return HttpResponseRedirect(reverse('my-pets'))

        return HttpResponseRedirect(reverse('my-pets'))


# Delete Exist Pet
@login_required(login_url='user_login')
def my_pets_delete(request,petId):
    try:
        if petId:
            pet = Pet.objects.get(id=petId)
            pet.delete()
            return HttpResponseRedirect(reverse('my_proposal'))
    except Pet.DoesNotExist as e:
        return HttpResponseRedirect(reverse('my_proposal'))



def my_vetcoins(request):
    user_profile = request.user.userprofile
    details = user_profile.vetcoinObj[0]['outputValues']['details']
    data = {}
    if details:
        data = details
    return render(request,'pawtectApp/my-vetcoins.html',{"details":data})

def page_not_found(request):
    return render(request,'pawtectApp/404.html')


# Get All Proposal
@login_required(login_url='user_login')
def my_proposal(request):
    user_profile = request.user.userprofile
    petId = request.GET.get('petId',None)
    myPets = Pet.objects.filter(user_profile=user_profile).order_by('id')
    selectedPet = None
    if petId:
        selectedPet = Pet.objects.get(pk=petId)
        pets = [selectedPet]
    else:
        pets = myPets

    for petBirth in pets:
        diffrence = today - petBirth.birthDate
        actualDays = diffrence.days
        if actualDays < const.SMALL_AGE_LIMIT or actualDays > const.MAX_AGE_LIMIT:
            petBirth.disabledClass = True
        else:
            petBirth.disabledClass = False
    questions = Questions.objects.all().order_by('id')
    return render(request,"pawtectApp/my-proposal.html",{"pets":pets,"questions":questions,"myPets":myPets,"selectedPet":selectedPet})


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
        allOptions = ''
        arr = []
        try:
            queObj = PetQuestion.objects.get(Q(pet_id=request.POST['petId']) & Q(questions_id=request.POST['questionId']))
            queObj.answer = request.POST['answer']
            queObj.save()
            healthAnswers = PetQuestion.objects.filter(pet_id=request.POST['petId'])
            for ans in healthAnswers:
                allOptions = ans.questions.option
                allQAns = ans.answer
                for op in allOptions:
                    if allQAns == op['name']:
                        arr.append(op["is_insurance_allowed"])
                        sumarray = sum(arr)
            return JsonResponse({"sumarray":sumarray,"petId":request.POST['petId']})

        except PetQuestion.DoesNotExist:
            new_values = {'pet_id':request.POST['petId'],'questions_id':request.POST['questionId'],'answer':request.POST['answer']}
            queObj = PetQuestion(**new_values)
            queObj.save()
            healthAnswers = PetQuestion.objects.filter(pet_id=request.POST['petId'])
            for ans in healthAnswers:
                allOptions = ans.questions.option
                allQAns = ans.answer
                for op in allOptions:
                    if allQAns == op['name']:
                        arr.append(op["is_insurance_allowed"])
                        sumarray = sum(arr)
            return JsonResponse({"sumarray":sumarray,"petId":request.POST['petId']})

# To get plan fees
@csrf_exempt
def planFees(request):
    if request.method == "POST":
        fees = Plans.objects.filter(Q(category=request.POST['category']) & Q(age__age_range=request.POST['age']) & Q(type__name = request.POST['planType']) & Q(coverage_amount__amount = request.POST['coverage_amount'])).values()
        if fees:
            newFees = list(fees)
            for i in newFees:
                return JsonResponse({"fees":i})
        else:
            return HttpResponse("NOT FOUND.")
    else:
        return HttpResponse("NOT POST METHOD.")


    

