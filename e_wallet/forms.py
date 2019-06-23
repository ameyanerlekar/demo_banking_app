from django import forms
from .models import Client
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class CustomUserRegistrationForm(forms.Form):
	first_name = forms.CharField(label = "First Name", max_length = 15, required = True)
	last_name = forms.CharField(label = "Last Name", max_length = 15, required = True)
	username = forms.CharField(label = "Set Your Username", required = True)
	emailId = forms.EmailField(label = "Enter Email ID", required = True)
	password1 = forms.CharField(label = "Set a Password", required = True, widget = forms.PasswordInput)
	password2 = forms.CharField(label = "Please Confirm Your Password", required = True, widget = forms.PasswordInput)
	address = forms.CharField(label = "Enter Your Address", required = True)
	
	def clean_username(self):
		username = self.cleaned_data.get("username")
		user = User.objects.filter(username = username)
		if len(user) != 0:
			raise ValidationError("Sorry, this username already exists. Please select another one.")
		return username
		
	def clean_email(self):
		email = self.cleaned_data.get("email")
		user = User.objects.filter(email = email)
		if len(user) != 0:
			raise ValidationError('This email is already in use! If you have forgotten your password, please click on "Forgot Password" link to reset your password.')
		return email
		
	def clean_passwords(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 == password2:
			return password1
		else:
			raise ValidationError("Sorry, the passwords do not match.")
		
	def save(self, commit = True):
		user = User.objects.create_user(
			username = self.cleaned_data.get("username"),
			password = self.cleaned_data.get("password1"),
			first_name = self.cleaned_data.get("first_name"),
			last_name = self.cleaned_data.get("last_name")
		)
		
		client = Client.objects.create(
			username = self.cleaned_data.get("username"),
			first_name = self.cleaned_data.get("first_name"),
			last_name = self.cleaned_data.get("last_name"),
			address = self.cleaned_data.get("address")
		)
		
		return user