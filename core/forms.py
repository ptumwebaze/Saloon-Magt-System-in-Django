# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import employee, order, service, orderdetail, cart, expense

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "firstname",                
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "lastname",                
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email  address",                
                "class": "form-control"
            }
        ))
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']


class employee_up(forms.ModelForm):
    class Meta:
        model = employee
        fields = ['name','contact','email','position']

class serviceup(forms.ModelForm):
    class Meta:
        model = service
        fields = ['name','selling_price','commission','cost_price']

class expenseup(forms.ModelForm):
    class Meta:
        model = expense
        fields = ['name','amount','description']

class cartup(forms.ModelForm):
    class Meta:
        model = cart
        fields = ['service','service_price','staff','added_by']


class orderup(forms.ModelForm):
    class Meta:
        model = order
        fields = ['customer','customer_phone','amount','paid','mode','balance','added_by']


class orderdetailup(forms.ModelForm):
    class Meta:
        model = orderdetail
        fields = ['service','service_price','order_id','added_by']



