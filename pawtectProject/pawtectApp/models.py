from django.db import models
from django.contrib.postgres.fields import JSONField,ArrayField
from django.contrib.auth.models import User
from django.utils import timezone

QUESTION_TYPE_CHOICES = [
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
        ('text', 'Text')
    ]
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = 'media/', default = '/assets/img/common-images/avatar.png')
    mobile = models.BigIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=50,blank=True, null=True)
    address1= models.CharField(max_length=100,blank=True, null=True)
    address2= models.CharField(max_length=100,blank=True, null=True)
    area= models.CharField(max_length=50,blank=True, null=True)
    city= models.CharField(max_length=50,blank=True, null=True)
    country= models.CharField(max_length=100,blank=True, null=True)
    pincode=models.CharField(max_length=10,blank=True, null=True)
    profession= models.TextField(blank=True, null=True)


    def __str__(self):
         return self.user.username

class UpdateBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)


class Settings(models.Model):
    key = models.CharField(max_length=100,unique=True)
    value = JSONField(blank=True, null=True)
   

class Age(models.Model):
    age_range = models.CharField(max_length=50,blank=True, null=True)
    start_age = models.CharField(max_length=50,default=0)
    end_age = models.CharField(max_length=50,default=0)

    DAYS = 'D'
    WEEKS = 'W'
    MONTHS = 'M'
    YEARS = 'Y'
    AGE_UNIT_CHOICES = [
        (DAYS, 'Days'),
        (WEEKS, 'Weeks'),
        (MONTHS, 'Months'),
        (YEARS, 'Years'),
    ]

    start_age_unit = models.CharField(max_length=50, choices=AGE_UNIT_CHOICES)
    end_age_unit = models.CharField(max_length=50, choices=AGE_UNIT_CHOICES)

    def __str__(self):
        return self.age_range

class Type(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)
    icon = models.CharField(max_length=50,blank=True, null=True)
    features = JSONField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Coverage_Amount(models.Model):
    amount = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.amount)


class Plans(UpdateBaseModel):
    category = models.CharField(max_length=100, blank=True, null=True)
    type = models.ForeignKey(Type, blank=True, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True, null=True)
    features = JSONField(blank=True, null=True)
    age = models.ManyToManyField(Age)
    coverage_amount = models.ForeignKey(Coverage_Amount,blank=True, null=True, on_delete=models.CASCADE)
    fees = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.category

class Questions(UpdateBaseModel):
    question = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES,default='text')
    option = JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.question

class Pet(UpdateBaseModel):
    name = models.CharField(max_length=50,blank=True, null=True)
    catagory = models.CharField(max_length=50,blank=True, null=True)
    picture = models.ImageField(upload_to = 'media/', default = '/assets/img/common-images/avatar.png')
    microchip_Number = models.CharField(max_length=50,blank=True, null=True)
    species = models.CharField(max_length=100, blank=True, null=True)
    breed = models.CharField(max_length=100,blank=True, null=True)
    birthDate = models.DateField(auto_now=False)
    gender = models.CharField(max_length=50,blank=True, null=True)
    consult_Name = models.CharField(max_length=100,blank=True, null=True)
    consult_Email = models.EmailField(max_length=254,blank=True, null=True)
    consult_mobileNumber = models.CharField(max_length=30,blank=True, null=True)
    consult_Address = models.CharField(max_length=500,blank=True, null=True)
    question_answer = JSONField(blank=True, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name

    def get_answer(self,question_id):
        try:
            answer = PetQuestion.objects.get(pet_id=self.id,questions_id=question_id).answer
            return answer
        except Exception as e:
            return None
        return None

    


class PetQuestion(models.Model):
    answer = models.CharField(max_length=100)
    pet = models.ForeignKey(Pet,on_delete=models.CASCADE)
    questions = models.ForeignKey(Questions,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pet)
