# banking/views.py
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_account(request):
    # Создаем новый банковский счет для текущего пользователя
    new_account = Account.objects.create(user=request.user, balance=0, is_locked=False)
    serializer = AccountSerializer(new_account)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_accounts(request):
    # Получаем все счета в системе
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_transactions(request):
    # Получаем все транзакции в системе
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_transaction(request):
    if request.method == 'POST':
        sender_account = get_object_or_404(Account, user=request.user)
        receiver_username = request.data.get('receiver_username')
        amount = Decimal(request.data.get('amount', 0))

        # Валидация и логика проведения транзакции
        try:
            receiver_account = Account.objects.get(user__username=receiver_username)
            if sender_account.is_locked or receiver_account.is_locked:
                raise ValueError("Одна из учетных записей заблокирована.")
            if sender_account.balance < amount:
                raise ValueError("Недостаточно средств")
            
            # Создаем транзакцию
            transaction = Transaction.objects.create(sender=sender_account, receiver=receiver_account, amount=amount)
            
            # Обновляем балансы счетов
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()
            
            serializer = TransactionSerializer(transaction)
            return Response({'success': True, 'transaction': serializer.data})
        except Account.DoesNotExist:
            return Response({'success': False, 'error': 'Учетная запись получателя не найдена'})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)})

    return Response({'success': False, 'error': 'Недопустимый метод запроса'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_transactions(request, account_id):
    # Получаем все транзакции для конкретного счета
    account = get_object_or_404(Account, id=account_id)
    transactions = Transaction.objects.filter(sender=account)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    if request.method == 'POST':
        user_account = get_object_or_404(Account, user=request.user)
        amount = Decimal(request.data.get('amount', 0))


        # Валидация и логика пополнения счета
        try:
            # amount = float(amount)
            if amount <= 0:
                raise ValueError("Сумма должна быть больше нуля.")

            # Создаем транзакцию
            transaction = Transaction.objects.create(sender=user_account, receiver=user_account, amount=amount)

            # Обновляем баланс счета
            user_account.balance += amount
            user_account.save()

            serializer = TransactionSerializer(transaction)
            return Response({'success': True, 'transaction': serializer.data})
        except ValueError as e:
            return Response({'success': False, 'error': str(e)})

    return Response({'success': False, 'error': 'Недопустимый метод запроса'})