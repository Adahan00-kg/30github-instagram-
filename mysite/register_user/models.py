from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


STATUS_ACC = (
    ('закрытый','закрытый'),
    ('открытый','открытый'),
)

CHOICES_GENDER = (
    ('женский','женский'),
    ('мужской','мужской'),
    ('другой','другой'),
    ('предпочитаю не указывать','предпочитаю не указывать')
)

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True,blank=True,unique=True)
    date_register = models.DateTimeField(auto_now_add=True,verbose_name='Когда человек зарегистрировался')
    profile_picture = models.ImageField(upload_to='profile_img',null=True,blank=True)
    status_acc = models.CharField(max_length=15,choices=STATUS_ACC,default='открытый')
    age = models.DateField(null=True,blank=True)
    bio = models.CharField(max_length=150,null=True,blank=True)
    gender = models.CharField(max_length=55,choices=CHOICES_GENDER,default='предпочитаю не указывать')


    def __str__(self):
         return f'{self.username} - {self.first_name}'


class Network(models.Model):
    network_name = models.CharField(max_length=55)
    network_link = models.URLField(null=True,blank=True)
    user_connect = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='network')

    def __str__(self):
        return f'{self.network_name}'

