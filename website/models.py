import numpy as np
from django.db import models
import pandas as pd




class CarFormResult(models.Model):
    fuel_type = models.CharField(max_length=255)
    transmission = models.CharField(max_length=250)
    owner_type = models.CharField(max_length=255)
    mileage = models.FloatField()
    engine = models.FloatField()
    power = models.FloatField()
    seats = models.IntegerField()
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    year = models.IntegerField()
    kilometers_driven = models.IntegerField()
    predicted_price = models.FloatField()

   
    
 





class UploadedFormData(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10)
    car_model = models.CharField(max_length=255)
    car_year = models.IntegerField()
    mileage = models.IntegerField()
    kilometers_driven = models.IntegerField()
    person_image = models.ImageField(upload_to='person_images/')
    car_image = models.ImageField(upload_to='car_images/')

    

# models.py

from django import forms

class ContactForm(models.Model):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    contact_number = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea)


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
