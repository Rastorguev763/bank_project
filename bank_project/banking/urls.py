# banking/urls.py
from django.urls import path
from .views import create_account, all_accounts, all_transactions, make_transaction, account_transactions, deposit

urlpatterns = [
    path('api/create_account/', create_account, name='api_create_account'),
    path('api/all_accounts/', all_accounts, name='api_all_accounts'),
    path('api/all_transactions/', all_transactions, name='api_all_transactions'),
    path('api/make_transaction/', make_transaction, name='api_make_transaction'),
    path('api/account_transactions/<int:account_id>/', account_transactions, name='api_account_transactions'),
    path('api/deposit/', deposit, name='api_deposit'),
]
