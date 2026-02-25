from django import forms
from .models import Transaction
from datetime import date


class TransactionForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        initial=date.today
    )

    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'date', 'category', 'description', 'payment_method']


from .models import Loan, LoanPerson


class LoanForm(forms.ModelForm):

    person_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter person name'
        })
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Loan
        fields = ['person_name', 'type', 'amount', 'date', 'description']

    def save(self, commit=True, user=None):
        name = self.cleaned_data['person_name']

        person, created = LoanPerson.objects.get_or_create(
            user=user,
            name=name
        )

        loan = super().save(commit=False)
        loan.user = user
        loan.person = person

        if commit:
            loan.save()

        return loan
    
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']