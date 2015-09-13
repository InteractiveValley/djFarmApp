# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *
from django.forms.extras.widgets import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ( "username", "email" )

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise ValidationError("Email already exists")
		return email

	def clean(self):
		form_data = self.cleaned_data
		if form_data['password'] != form_data['password']:
			self._errors["password"] = "Password do not match"
			del form_data['password']
		return form_data

    def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class' : 'form-control', 'required': 'required'})
		self.fields['email'].widget.attrs.update({'class' : 'form-control', 'required': 'required'})
		self.fields['password1'].widget.attrs.update({'class' : 'form-control', 'required': 'required'})
		self.fields['password2'].widget.attrs.update({'class' : 'form-control', 'required': 'required'})