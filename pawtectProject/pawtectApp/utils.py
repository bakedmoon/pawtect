from django.core.mail import send_mail, BadHeaderError
import json
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import Pet
from pawtectProject import settings


def sendMailToUser(toEmail,name):
    subject = "Thanks for contact us!"
    message = "We will contact you in few moments"
    toEmail = toEmail
    send_mail(subject, message,'',[toEmail])


def default_data():
    breed = open(settings.ASSETS+'/default/breeds.json')
    return json.load(breed)


def get_filter_params(params,filterParams={},popList=[]):
    for p in params:
        par=params[p]
        if ',' in par:
            par=par.split(",")
        filterParams[p] =par
    filterParams.pop('1',1)
    filterParams.pop('limit',1)
    filterParams.pop('page',1)
    for p in popList:
        filterParams.pop(p,None)
    return filterParams


def default_data_country():
    country = open(settings.ASSETS+'/default/country.json')
    return json.load(country)

def make_image_url(url):
    myfile = url
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    imageUrl = fs.url(filename)
    return imageUrl

# Check Microchip Number Exist
def checkMicrochipNumber(microchipNumber):
    existChipNumber = Pet.objects.filter(microchip_Number = microchipNumber).exists()
    return existChipNumber

#Get fill pet info using from views.my_pets_new funtion.
def afterErrorPetData(petInfo):
    pet = {}
    pet['name'] = petInfo['name']
    pet['microchip_Number'] = petInfo['microchip_Number']
    pet['species'] = petInfo['species']
    pet['breed'] = petInfo['breed']
    pet['birthDate'] = petInfo['birthDate']
    pet['gender'] = petInfo.get('gender', '')
    pet['consult_Name'] = petInfo['consult_Name']
    pet['consult_Email'] = petInfo['consult_Email']
    pet['consult_mobileNumber'] = petInfo['consult_mobileNumber']
    pet['consult_Address'] = petInfo['consult_Address']
    return pet

