# test_views.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from decimal import Decimal
from banking.models import Account, Transaction

@pytest.fixture
def user_client(transactional_db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def create_account(user_client):
    response = user_client.post('/api/create_account/')
    return response.data['id']

@pytest.fixture
def create_receiver_account(user_client):
    receiver = User.objects.create_user(username='receiver', password='receiverpassword')
    receiver_client = APIClient()
    receiver_client.force_authenticate(user=receiver)
    response = receiver_client.post('/api/create_account/')
    return response.data['id']

def test_create_account(user_client):
    response = user_client.post('/api/create_account/')
    assert response.status_code == 200
    assert 'id' in response.data

def test_all_accounts(user_client, create_account):
    response = user_client.get('/api/all_accounts/')
    assert response.status_code == 200
    assert len(response.data) > 0

def test_all_transactions(user_client):
    response = user_client.get('/api/all_transactions/')
    assert response.status_code == 200
    assert len(response.data) == Transaction.objects.count()


def test_account_transactions(user_client, create_account):
    account_id = create_account
    response = user_client.get(f'/api/account_transactions/{account_id}/')
    assert response.status_code == 200
    assert len(response.data) == Transaction.objects.filter(sender__id=account_id).count()

# def test_deposit(user_client):
    # amount = 100
    # data = {'amount': amount}
    # response = user_client.post('/api/deposit/', data=data)
    # print(response)
    # print(response.data)
    # assert response.status_code == 200
    # assert response.data['success'] is True
    # assert 'transaction' in response.data
    # assert Account.objects.get(user=user_client.user).balance == Decimal(amount)

def test_make_transaction(user_client, create_account, create_receiver_account):
    amount = 5
    data = {'receiver_username': 'receiver', 'amount': amount}
    response = user_client.post('/api/make_transaction/', data=data)
    assert response.status_code == 200
    assert response.data['success'] is False
    assert 'error' in response.data