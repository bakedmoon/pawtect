from django.contrib.auth.models import User
from pawtectApp.models import UserProfile
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

    def otpVerify(self,otp,mobile):
        otp = 123456
        user = User.objects.get(username=mobile)
        if otp == otp:
            user_is_active = True
            user.save()
            return user
            
