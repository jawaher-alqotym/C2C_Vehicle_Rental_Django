
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class UserCredential(models.Model):
    '''
    this model job is to add another attrib to auth.model.user: driver_licence, phone_number
    '''
    user = models.OneToOneField(User, related_name= 'user_credential',on_delete=models.CASCADE, null=True)
    joining_date = models.DateTimeField(auto_now_add=True)
    driver_licence = models.ImageField(upload_to="images/driver_licence")
    phone_number = PhoneNumberField(unique=True)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0, help_text='The vehicle owner/rentee ratings average')

    def __str__(self):
        return f'{self.user}'


