from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Wallet
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
import openpyxl
from django.http import HttpResponse

@login_required
def dashboard(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    context = {
        "wallet": wallet
    }

    return render(request, "dashboard.html", context)


from .forms import TransactionForm
from django.shortcuts import redirect


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, "add_transaction.html", {"form": form})

from .forms import LoanForm
from .models import Loan
from django.db.models import Sum


@login_required
def add_loan(request):
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('dashboard')
    else:
        form = LoanForm()

    return render(request, "add_loan.html", {"form": form})


@login_required
def all_loans(request):
    loans = Loan.objects.filter(user=request.user).order_by('-date')

    total_given = loans.filter(type='GIVEN').aggregate(Sum('amount'))['amount__sum'] or 0
    total_taken = loans.filter(type='TAKEN').aggregate(Sum('amount'))['amount__sum'] or 0
    total_received = loans.filter(type='RECEIVED').aggregate(Sum('amount'))['amount__sum'] or 0

    pending = (total_given - total_received) - total_taken

    return render(request, "all_loans.html", {
        "loans": loans,
        "total_given": total_given,
        "total_taken": total_taken,
        "total_received": total_received,
        "pending": pending
    })


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from .models import Transaction, Wallet, Loan


@login_required
def dashboard(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    today = date.today()

    monthly_transactions = Transaction.objects.filter(
        user=request.user,
        date__month=today.month,
        date__year=today.year
    )

    total_income = monthly_transactions.filter(
        type='INCOME'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expense = monthly_transactions.filter(
        type='EXPENSE'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    savings = total_income - total_expense

    loans = Loan.objects.filter(user=request.user)

    total_given = loans.filter(type='GIVEN').aggregate(Sum('amount'))['amount__sum'] or 0
    total_taken = loans.filter(type='TAKEN').aggregate(Sum('amount'))['amount__sum'] or 0
    total_received = loans.filter(type='RECEIVED').aggregate(Sum('amount'))['amount__sum'] or 0

    pending = total_taken - total_received

    return render(request, "dashboard.html", {
        "wallet": wallet,
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": savings,
        "total_given": total_given,
        "total_taken": total_taken,
        "total_received": total_received,
        "pending": pending,
    })



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    return render(request, 'dashboard.html', {'wallet': wallet})


from django.contrib.auth.decorators import login_required

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transaction_history.html', {
        'transactions': transactions
    })

@login_required
def monthly_report(request):
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    transactions = Transaction.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    )

    total_income = transactions.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'monthly_report.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'net': total_income - total_expense
    })

@login_required
def export_monthly(request):
    now = timezone.now()
    transactions = Transaction.objects.filter(
        user=request.user,
        date__month=now.month,
        date__year=now.year
    )

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Monthly Transactions"

    sheet.append(["Date", "Type", "Amount", "Category", "Description", "Payment"])

    for t in transactions:
        sheet.append([
            t.date.strftime("%d-%m-%Y"),
            t.type,
            float(t.amount),
            t.category,
            t.description,
            t.payment_method
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename=monthly_report.xlsx'
    workbook.save(response)

    return response