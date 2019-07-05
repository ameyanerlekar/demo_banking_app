from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from.forms import CustomUserRegistrationForm, TransactionForm, GetStatementForm
from .models import Client, Account, Transaction
from django.db.models import Q
import datetime

def render_home(request):
	if request.method != "POST" and not request.user.is_authenticated:
		form = AuthenticationForm()
		return render(request, "home.html", {"form": form, "button": "Sign In"})
	elif request.user.is_authenticated:
		client = Client.objects.get(username = request.user.username)
		accounts = Account.objects.filter(owner = client.username)
		transaction_form = TransactionForm()
		statement_form = GetStatementForm()
		return render(request, "homepage.html", {"username": client.first_name + " " + client.last_name, "button": "Sign out", "accounts": accounts, "transaction_form": transaction_form, "statement_form": statement_form})			
	else:
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				#print(user.username)
				try:
					client = Client.objects.get(username = user.username)
					accounts = Account.objects.filter(owner = client.username)
					transaction_form = TransactionForm()
					statement_form = GetStatementForm()
					return render(request, "homepage.html", {"username": client.first_name + " " + client.last_name, "button": "Sign out", "accounts": accounts, "transaction_form": transaction_form, "statement_form": statement_form})			
				except:
					return redirect("/admin")
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
			statement_form = GetStatementForm()
			login(request, user)
			return render(request, "homepage.html", {"username": client.first_name + " " + client.last_name, "button": "Sign out", "accounts": accounts, "transaction_form": transaction_form, "statement_form": statement_form})			
		else:
			return render(request, "sign_up.html", {"message": form.errors, "form": form})
		
def make_transaction(request):
	if request.method == "POST" and request.user.is_authenticated:
		transaction_form_particulars = TransactionForm(request.POST)
		from_account = request.POST.get("from_account")
		transaction_amount = request.POST.get("transaction_amount")
		beneficiary_account = request.POST.get("beneficiary_account")
		beneficiary_name = request.POST.get("beneficiary_name")
		remarks = request.POST.get("remarks")
		transaction_time = datetime.datetime.now()
		account_to_debit = Account.objects.get(account_number = from_account)
		account_to_credit = Account.objects.get(account_number = beneficiary_account)
		if (account_to_credit.owner.first_name + " " + account_to_credit.owner.last_name).lower() == beneficiary_name.lower() and not account_to_credit.is_frozen and not account_to_debit.is_frozen:
			try:
				account_to_debit.debit(int(transaction_amount))
				account_to_credit.credit(int(transaction_amount))
				transaction = Transaction.objects.create(
					time = transaction_time,
					from_account = from_account,
					transaction_amount = transaction_amount,
					beneficiary_account = beneficiary_account,
					beneficiary_name = beneficiary_name,
					remarks = remarks
				)
				client = Client.objects.get(username = request.user.username)
				accounts = Account.objects.filter(owner = client.username)
				transaction_form = TransactionForm()
				statement_form = GetStatementForm()
				return render(request, "homepage.html", {"username": client.first_name + " " + client.last_name, "button": "Sign out", "accounts": accounts, "transaction_form": transaction_form, "statement_form": statement_form})
			except Exception as e:
				return HttpResponse("<p style='color:red;'>" + str(e) + "</p>")
		else:
			return HttpResponse("<p style = 'color:red;'>Sorry, the name of the account holder, to whom you wish to transfer funds, as entered by you, did not match our records. Please retry with the correct name.</p>")
	else:
		return HttpResponse("<p style = 'color=red;'>Unauthorized Transaction. Please sign in <a href='/home'>here</a> to continue.")

def get_statement(request):
	if request.user.is_authenticated:
		for_account = request.POST.get("for_account")
		all_account_transactions = Transaction.objects.filter((Q(from_account = for_account) | Q(beneficiary_account = for_account)))
		valid_transactions = []
		FROM_DATE = datetime.datetime.strptime(request.POST.get("from_date"), "%m/%d/%Y").date()
		TO_DATE = datetime.datetime.strptime(request.POST.get("to_date"), "%m/%d/%Y").date()
		for transaction in all_account_transactions:
			if transaction.time.date() >= FROM_DATE and transaction.time.date() <= TO_DATE:
				valid_transactions.append(transaction)
		owner = request.user.first_name + " " + request.user.last_name		
		return render(request, "transactions_test.html", {"transactions": valid_transactions, "owner": owner, "for_account": for_account})#, "from_date": FROM_DATE, "to_date": TO_DATE))
		
		
def forms_test(request):
	forms = []
	for i in range(3):
		forms.append(GetStatementForm())
	return render(request, "forms_test.html", {"forms": forms})