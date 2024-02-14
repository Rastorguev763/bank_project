# Banking System API

Этот проект представляет собой API для банковской системы, который позволяет пользователям создавать счета, проводить транзакции и управлять своими финансами.

В проекте создана тестовая база с 2-я аккаунтами

**admin : admin**

**test : !1Qwerty1234**

Чтобы создать свою, удалите `bank_project/db.sqlite3` и `bank_project/banking/migrations`, а дальше по инструкции.

## Установка

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/Rastorguev763/bank_project.git
   ```

    Перейти в деректорию

    ```bash
    cd bank_project
    ```

2. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

    Перейти в деректорию с проектом

   ```bash
   cd bank_project
   ```

3. Применить миграции:

   ```bash
   python manage.py migrate
   ```

4. Запустить сервер:

   ```bash
   python manage.py runserver
   ```

5. API будет доступно по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Использование

- Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

Следуйте инструкциям на экране для создания учетной записи суперпользователя Django.

- Запустите сервер разработки Django:

```bash
python manage.py runserver
```

Откройте браузер и перейдите по адресу <http://127.0.0.1:8000/admin/>.

Войдите в админ-панель с использованием учетных данных суперпользователя.

В админ-панели создайте нового пользователя, которого вы планируете использовать для тестирования.

Получите токен для созданного пользователя.

## Примеры запросов

Обратите внимание, что вам нужно заменить `'YOUR_ACCESS_TOKEN'` на действующий токен доступа.

1. **Создание банковского счета:**

```
POST /api/create_account/
```

```python
import requests

headers = {
    'Authorization': 'Token YOUR_ACCESS_TOKEN',
}

curl = 'http://127.0.0.1:8000/api/create_account/'

response = requests.post(curl, headers=headers)

print(response.status_code)
print(response.json())
```

2. **Получение списка всех счетов:**

```
GET /api/all_accounts/
```

```python
import requests

headers = {
    'Authorization': 'Token YOUR_ACCESS_TOKEN',
}

curl = 'http://127.0.0.1:8000/api/all_accounts/'

response = requests.get(curl, headers=headers)

print(response.status_code)
print(response.json())
```

3. **Создание транзакции:**

```
POST /api/make_transaction/
```

Параметры запроса:

- `receiver_username`: Имя пользователя-получателя
- `amount`: Сумма транзакции

```python
import requests

headers = {
    'Authorization': 'Token YOUR_ACCESS_TOKEN',
}

data = {"receiver_username": "admin", "amount": 50}

curl = 'http://127.0.0.1:8000/api/make_transaction/'

response = requests.post(curl, headers=headers, data=data)

print(response.status_code)
print(response.json())
```

4. **Пополнение счета:**

```
POST /api/deposit/
```

Параметры запроса:

- `amount`: Сумма пополнения

```python
import requests

headers = {
    'Authorization': 'Token YOUR_ACCESS_TOKEN',
}

data = {'amount': 100.0}

curl = 'http://127.0.0.1:8000/api/deposit/'

response = requests.post(curl, headers=headers, data=data)

print(response.status_code)
print(response.json())
```

5. **Получение транзакций для конкретного счета:**

```
GET /api/account_transactions/{account_id}/
```

- `account_id`: ID аккаунта по которому нужно просмотреть информацию

```python
import requests

headers = {
    'Authorization': 'Token YOUR_ACCESS_TOKEN',
}

account_id = 1  # Замените на конкретный ID счета

curl = f'http://127.0.0.1:8000/api/account_transactions/{account_id}/'

response = requests.get(curl, headers=headers)

print(response.status_code)
print(response.json())
```

6. **Получение списка всех транзакций:**

  ```
  GET /api/all_transactions/
  ```

```python
import requests

headers = {
    'Authorization': 'Token YOUR_ACCESS_TOKEN',
}

curl = 'http://127.0.0.1:8000/api/all_transactions/'

response = requests.get(curl, headers=headers)

print(response.status_code)
print(response.json())
```

## Тестирование

Запустить тесты:

```bash
pytest views_tests.py
```

## Задание

### Описание

Цель данного задания - разработка банковского сервиса на основе Django с использованием API для управления банковскими счетами и транзакциями. Проект должен обеспечивать безопасность операций, включая взаимную блокировку счетов.

## Задачи

### Реализация API:

- Создание нового банковского счета.
- Просмотр всех счетов в системе.
- Просмотр всех транзакций в системе.
- Проведение транзакции между счетами.
- Просмотр всех транзакций для конкретного счета.

### Обеспечение корректной работы операций:

- Проверка существования отправителя и получателя.
- При создании счета, баланс должен быть равен 0.
- Обновление балансов счетов при проведении транзакции.
- Обработка случаев недостаточного баланса у отправителя.
- Ведение истории транзакций для каждого счета.
- Возможность блокировки счетов.
