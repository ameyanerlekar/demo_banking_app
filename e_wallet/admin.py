from django.contrib import admin
from .models import Client, Account, Transaction

# Register your models here.
admin.site.register(Client)
admin.site.register(Account)
admin.site.register(Transaction)

