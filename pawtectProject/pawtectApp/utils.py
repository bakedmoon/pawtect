from django.core.mail import send_mail, BadHeaderError
import json
from pawtectProject import settings


def sendMailToUser(toEmail,name):
    subject = "Thanks for contact us!"
    message = "We will contact you in few moments"
    toEmail = toEmail
    send_mail(subject, message,'',[toEmail])


def default_data():
    breed = open(settings.ASSETS+'/default/breeds.js','r').read()
    return breed

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