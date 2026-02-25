from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('add-loan/', views.add_loan, name='add_loan'),
    path('all-loans/', views.all_loans, name='all_loans'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('transactions/', views.transaction_history, name='transactions'),
    path('export-monthly/', views.export_monthly, name='export_monthly'),
    path('monthly-report/', views.monthly_report, name='monthly_report'),
]