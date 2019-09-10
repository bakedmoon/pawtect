from django.core.mail import send_mail, BadHeaderError
import json
from django.core.files.storage import FileSystemStorage
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
    print("THE PARAMS ARE HERE COME FOR FILTER-->>",params)
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