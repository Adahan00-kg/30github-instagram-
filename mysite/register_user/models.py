from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


STATUS_ACC = (
    ('закрытый','закрытый'),
    ('открытый','открытый'),
)

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True,blank=True,unique=True)
    date_register = models.DateTimeField(auto_now_add=True,verbose_name='Когда человек зарегистрировался')
    profile_picture = models.ImageField(upload_to='profile_img',null=True,blank=True)
    status_acc = models.CharField(max_length=15,choices=STATUS_ACC,default='открытый')
    age = models.DateField(null=True,blank=True)

