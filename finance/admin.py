from django.contrib import admin
from .models import Wallet, Transaction, LoanPerson, Loan


admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(LoanPerson)
admin.site.register(Loan)