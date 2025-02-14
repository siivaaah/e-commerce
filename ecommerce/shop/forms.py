from django import forms

from django.contrib.auth.management.commands.changepassword import UserModel
from django.forms import PasswordInput

class Registerform(forms.ModelForm):
    password=forms.CharField(widget=PasswordInput)
    class Meta:
        model=UserModel
        fields=['username','password','email','first_name','last_name']