from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from.forms import CustomUserRegistrationForm, TransactionForm
from .models import Client, Account

def render_home(request):
	if request.method != "POST":
		form = AuthenticationForm()
		return render(request, "home.html", {"form": form, "button": "Sign In"})
	else:
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				#print(user.username)
				client = Client.objects.get(username = user.username)
				accounts = Account.objects.filter(owner = client.username)
				transaction_form = TransactionForm()
				return render(request, "homepage.html", {"username": client.first_name + " " + client.last_name, "button": "Sign out", "accounts": accounts, "transaction_form": transaction_form})			
		else:
			return render(request, "home.html", {"message": "Invalid Credentials. Please try again!", "form": form, "button": "Sign In"})
				
def logout_user(request):
	logout(request)
	return redirect("home")
	
	
def sign_up(request):
	if request.method != "POST":
		form = CustomUserRegistrationForm()
		return render(request, "sign_up.html", {"form": form})
	else:
		form = CustomUserRegistrationForm(request.POST)
		print(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			#user = authenticate(username, password)
			client = Client.objects.get(username = username)
			accounts = Account.objects.filter(owner = username)
			transaction_form = TransactionForm()
			login(request, user)
			return render(request, "homepage.html", {"username": client.first_name + " " + client.last_name, "button": "Sign out", "accounts": accounts, "transaction_form": transaction_form})			
		else:
			return render(request, "sign_up.html", {"message": form.errors, "form": form})
		
