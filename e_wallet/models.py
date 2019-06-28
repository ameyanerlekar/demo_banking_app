from django.db import models
import datetime

# Create your models here.
from django.db import models
#from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
	username = models.CharField(max_length = 30, primary_key = True)
	first_name = models.CharField(max_length = 15)
	last_name = models.CharField(max_length = 15)
	address = models.TextField()
	
	def get_all_accounts(self):
		return Accounts.objects.filter(owner = self.get_username())
		
	def __str__(self):
		return self.first_name + " " + self.last_name + " (" + self.username + ")"
		

class Account(models.Model):
	account_number = models.CharField(max_length = 6, primary_key = True)
	account_balance = models.FloatField()
	owner = models.ForeignKey(Client, on_delete = models.CASCADE)
	is_frozen = models.BooleanField(default = False)
	
	def open(self):
		if not self.is_frozen:
			self.save()
			return "Account Created Successfully!"
		else:
			return "Sorry, your account, account no. " + str(self.account_number) + " has been temporarily frozen due for security reasons. Kindly visit your nearest branch for assistance."
			
	def close(self):
		if not self.is_frozen:
			self.delete()
			return "Account Deleted Successfully"
		else:
			return "Sorry, your account, account no. " + str(self.account_number) + " has been temporarily frozen due for security reasons. Kindly visit your nearest branch for assistance."

		
	def debit(self, debit_amount):
		if not self.is_frozen:
			if self.account_balance - debit_amount >=0:
				self.account_balance = self.account_balance - debit_amount
				self.save()
				return "Debited Rs. " + str(debit_amount) + " from account: " + str(self.account_number) + ". Remaining balance is Rs. " + str(self.account_balance) + "."
			else:
				raise Exception("Sorry! You do not have the necessary balance in this account to make this transfer. Please add funds to this account or use a different account with sufficient funds.")
		else:
			return "Sorry, your account, account no. " + str(self.account_number) + " has been temporarily frozen due for security reasons. Kindly visit your nearest branch for assistance."

		
	def credit(self, credit_amount):
		if not self.is_frozen:
			self.account_balance = self.account_balance + credit_amount
			self.save()
			return "Credited Rs. " + str(credit_amount) + " to account: " + str(self.account_number) + ". Available balance is Rs. " + str(self.account_balance) + "."
		else:
			return "Sorry, your account, account no. " + str(self.account_number) + " has been temporarily frozen due for security reasons. Kindly visit your nearest branch for assistance."
		
	def freeze(self):
		self.is_frozen = True
		
	def unfreeze(self):
		self.is_frozen = False
		
	def __str__(self):
		return str(self.account_number)
		
		
class Transaction(models.Model):
	id = models.AutoField(primary_key=True)
	time = models.DateTimeField()
	from_account = models.CharField(max_length = 10)
	transaction_amount = models.FloatField()
	beneficiary_account = models.CharField(max_length = 10)
	beneficiary_name = models.CharField(max_length = 20)
	remarks = models.TextField()