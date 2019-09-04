from django.contrib.auth.models import User
from pawtectApp.models import UserProfile
from django.core.files.storage import FileSystemStorage
class UserController():
    def userSignup(self,userInfo):
        user = User()
        user.first_name = userInfo['fname']
        user.last_name = userInfo['lname']
        user.email = userInfo['email']
        user.username = userInfo['mobile']
        user.set_password(userInfo.get('password2'))
        user.is_active = False
        user.save()
        return user

    def userProfile(self,userInfo,userId,myfile,uploadImage):
        print("THE AVATAR IS HERE-->>>",userInfo['avatar'])
        user = User.objects.get(pk=userId)
        user.first_name = userInfo['fname']
        user.last_name = userInfo['lname']
        user.email = userInfo['email']
        user.save()
        if uploadImage:
            imageUrl = userInfo['avatar']
        else:
            imageUrl = myfile
        userprofile  = UserProfile.objects.get(user_id=userId)
        userprofile.mobile = userInfo['mobile']
        userprofile.gender = userInfo['gender']
        userprofile.avatar = imageUrl
        userprofile.address1 = userInfo['address1']
        userprofile.area = userInfo['area']
        userprofile.city = userInfo['city']
        userprofile.country = userInfo['country']
        userprofile.pincode = int(userInfo['pincode'])
        userprofile.profession = []
        userprofile.save()
        return userprofile

    def otpVerify(self,otp,mobile):
        otp = 123456
        user = User.objects.get(username=mobile)
        if otp == otp:
            user_is_active = True
            user.save()
            return user
            
def make_image_url(url):
    myfile = url
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    imageUrl = fs.url(filename)
    return imageUrl