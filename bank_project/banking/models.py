# banking/models.py
from django.db import models
from django.contrib.auth.models import User

# Модель для представления банковского счета пользователя
class Account(models.Model):
    # Связь с встроенной моделью пользователя Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Баланс на счете пользователя (хранится как Decimal)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Флаг, указывающий, заблокирован ли счет
    is_locked = models.BooleanField(default=False)

    # Метод для удобного отображения объекта Account в административном интерфейсе
    def __str__(self):
        return f"Аккаунт: {self.user.username}"

# Модель для представления банковской транзакции между счетами
class Transaction(models.Model):
    # Ссылка на счет отправителя транзакции
    sender = models.ForeignKey(Account, related_name='sent_transactions', on_delete=models.CASCADE)
    
    # Ссылка на счет получателя транзакции
    receiver = models.ForeignKey(Account, related_name='received_transactions', on_delete=models.CASCADE)
    
    # Сумма транзакции (хранится как Decimal)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Дата и время создания транзакции
    timestamp = models.DateTimeField(auto_now_add=True)

    # Метод для удобного отображения объекта Transaction в административном интерфейсе
    def __str__(self):
        return f"Транзакция от {self.sender.user.username} для {self.receiver.user.username}"
