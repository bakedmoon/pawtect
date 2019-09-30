from django.contrib.auth.models import User
from pawtectApp.models import UserProfile
from django.http import HttpResponse
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from pawtectApp import utils

class UserController():
    def userSignup(self,userInfo):
        print("USER INFO IS HERE--->>>",userInfo)
        user = User()
        user.first_name = userInfo['fname']
        user.last_name = userInfo['lname']
        user.email = userInfo['email']
        user.username = userInfo['mobile']
        user.set_password(userInfo.get('password2'))
        user.is_active = False
        user.save()

        up = UserProfile()
        up.user_id = user.id
        up.mobile = userInfo['mobile']
        up.pincode = userInfo['pincode']
        up.selfRefer = userInfo['selfRefer']
        up.save()

        return user
       

    def userProfile(self,userInfo,userId,myfile,uploadImage):
            if uploadImage:
                imageUrl = utils.make_image_url(myfile)
            else:
                imageUrl = myfile
            user = User.objects.get(pk=userId)
            user.first_name = userInfo.get('fname',user.first_name)
            user.last_name = userInfo.get('lname',user.last_name)
            user.email = userInfo.get('email',user.email)
            user.save()

            userprofile  = UserProfile.objects.get(user_id=userId)
            userprofile.mobile = userInfo.get('mobile',userprofile.mobile)
            userprofile.gender = userInfo.get('gender',userprofile.gender)
            userprofile.avatar = imageUrl
            userprofile.address = userInfo.get('address',userprofile.address)
            userprofile.pincode = userInfo.get('pincode',userprofile.pincode)
            userprofile.city = userInfo.get('city',userprofile.city)
            userprofile.state = userInfo.get('state',userprofile.state)
            userprofile.country = userInfo.get('country',userprofile.country)
            userprofile.profession = userInfo.get('profession',userprofile.profession)
            userprofile.save()
            return userprofile
      
   