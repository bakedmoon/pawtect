from django.contrib.auth.models import User
from pawtectApp.models import Pet
from datetime import datetime
from django.http import HttpResponse
from pawtectApp import utils

class PetsController():
    def create_pet(self,petInfo,userProfile,myfile):
       
            birthDate = datetime.strptime(petInfo['birthDate'], '%B %d, %Y')
            imageUrl = ''
            if myfile is not '':
                imageUrl = utils.make_image_url(myfile)
            petObj = Pet()
            petObj.name = petInfo.get('name','')
            petObj.picture = imageUrl
            petObj.microchip_Number = petInfo.get('microchip_Number','')
            petObj.breed = petInfo.get('breed','')
            petObj.species = petInfo.get('species','')
            petObj.birthDate = birthDate
            petObj.gender = petInfo.get('gender', '')
            petObj.consult_Name = petInfo.get('consult_Name','')
            petObj.consult_Email = petInfo.get('consult_Email','')
            petObj.consult_mobileNumber = petInfo.get('consult_mobileNumber','')
            petObj.consult_Address = petInfo.get('consult_Address','')
            petObj.question_answer = ''
            petObj.user_profile = userProfile
            petObj.save()
            return petObj
       
            
    def update_pet(self,petInfo,userProfile,petId,myfile,uploadImage):
            birthDate = datetime.strptime(petInfo['birthDate'], '%B %d, %Y')
            if uploadImage:
                imageUrl = utils.make_image_url(myfile)
            else:
                imageUrl = myfile
            petObj = Pet.objects.get(id=petId)
            print("PET INFO IS HERE->>",petInfo.get('name'),petId)
            petObj.name = petInfo.get('name',petObj.name)
            petObj.picture = imageUrl
            petObj.microchip_Number = petInfo.get('microchip_Number',petObj.microchip_Number)
            petObj.breed = petInfo.get('breed',petObj.breed)
            petObj.species = petInfo.get('species',petObj.species)
            petObj.birthDate = birthDate
            petObj.gender = petInfo.get('gender', petObj.gender)
            petObj.consult_Name = petInfo.get('consult_Name',petObj.consult_Name)
            petObj.consult_Email = petInfo.get('consult_Email',petObj.consult_Email)
            petObj.consult_mobileNumber = petInfo.get('consult_mobileNumber',petObj.consult_mobileNumber)
            petObj.consult_Address = petInfo.get('consult_Address',petObj.consult_Address)
            petObj.question_answer = ''
            petObj.user_profile = userProfile
            petObj.save()
            return petObj
       

