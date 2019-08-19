from django.contrib.auth.models import User

class UserController():
    def userSignup(self,userInfo):
        userObj = User()
        userObj.first_name = userInfo['fname']
        userObj.last_name = userInfo['lname']
        userObj.email = userInfo['email']
        userObj.username = userInfo['mobile']
        userObj.password = userInfo['password2']
        userObj.is_active = False
        userObj.save()
        return userObj

    def otpVerify(self,otp,mobile):
        otp = 123456
        user = User.objects.get(username=mobile)
        if otp == otp:
            user.is_active = True
            user.save()
            return user
            
