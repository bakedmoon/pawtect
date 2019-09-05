from django.contrib.auth.models import User
from pawtectApp.models import Pet
from datetime import datetime
from pawtectApp import utils
import locale
class PetsController():
    def create_pet(self,petInfo,userProfile,myfile):
        locale.setlocale(locale.LC_ALL, '')
        birthDate = datetime.strptime(petInfo['birthDate'], '%B %d, %Y')
        imageUrl = utils.make_image_url(myfile)
        petObj = Pet()
        petObj.name = petInfo['name']
        petObj.picture = imageUrl
        petObj.microchip_Number = petInfo['microchip_Number']
        petObj.breed = petInfo['breed']
        petObj.species = petInfo['species']
        petObj.birthDate = birthDate
        petObj.gender = petInfo['gender']
        petObj.consult_Name = petInfo['consult_Name']
        petObj.consult_Email = petInfo['consult_Email']
        petObj.consult_mobileNumber = petInfo['consult_mobileNumber']
        petObj.consult_Address = petInfo['consult_Address']
        petObj.question_answer = ''
        petObj.user_profile = userProfile
        petObj.save()
        return petObj
            
    def update_pet(self,petInfo,userProfile,petId,myfile,uploadImage):
        locale.setlocale(locale.LC_ALL, '')
        birthDate = datetime.strptime(petInfo['birthDate'], '%B %d, %Y')
        if uploadImage:
            imageUrl = utils.make_image_url(myfile)
        else:
            imageUrl = myfile
        petObj = Pet.objects.get(id=petId)
        petObj.name = petInfo['name']
        petObj.picture = imageUrl
        petObj.microchip_Number = petInfo['microchip_Number']
        petObj.breed = petInfo['breed']
        petObj.species = petInfo['species']
        petObj.birthDate = birthDate
        petObj.gender = petInfo['gender']
        petObj.consult_Name = petInfo['consult_Name']
        petObj.consult_Email = petInfo['consult_Email']
        petObj.consult_mobileNumber = petInfo['consult_mobileNumber']
        petObj.consult_Address = petInfo['consult_Address']
        petObj.question_answer = ''
        petObj.user_profile = userProfile
        petObj.save()
        return petObj

