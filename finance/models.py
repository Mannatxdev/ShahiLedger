from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models import Sum



class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def total_balance(self):
        return self.bank_balance + self.cash_balance

    def __str__(self):
        return self.user.username



class Transaction(models.Model):

    TYPE_CHOICES = (
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    )

    PAYMENT_CHOICES = (
        ('BANK', 'Bank'),
        ('CASH', 'Cash'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            wallet, created = Wallet.objects.get_or_create(user=self.user)

            if self.type == 'INCOME':
                if self.payment_method == 'BANK':
                    wallet.bank_balance += self.amount
                else:
                    wallet.cash_balance += self.amount

            elif self.type == 'EXPENSE':
                if self.payment_method == 'BANK':
                    wallet.bank_balance -= self.amount
                else:
                    wallet.cash_balance -= self.amount

            wallet.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type} - {self.amount}"



class LoanPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Loan(models.Model):
    LOAN_TYPE = (
        ('GIVEN', 'Loan Given'),
        ('TAKEN', 'Loan Taken'),
        ('RECEIVED', 'Loan Received'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    person = models.ForeignKey(LoanPerson, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=LOAN_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None   # 🔥 Important check

        super().save(*args, **kwargs)

        # Only create transaction when NEW loan is created
        if is_new:
            if self.type == 'GIVEN':
                Transaction.objects.create(
                    user=self.user,
                    type='EXPENSE',
                    amount=self.amount,
                    date=self.date,
                    category='Loan Given',
                    description=f'Loan to {self.person.name}',
                    payment_method='CASH'
                )

            elif self.type in ['TAKEN', 'RECEIVED']:
                Transaction.objects.create(
                    user=self.user,
                    type='INCOME',
                    amount=self.amount,
                    date=self.date,
                    category='Loan Received',
                    description=f'Loan from {self.person.name}',
                    payment_method='CASH'
                )

    def __str__(self):
        return f"{self.person.name} - {self.type} - {self.amount}"
    

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)