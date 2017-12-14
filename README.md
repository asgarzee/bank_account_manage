Simple Implementation of Bank Transactions
---

This has APIs to create, list and retrieve bank accounts and perform money transfer across accounts and also debit and credit into an account.

It is using JWT for authentication

#### Requirements
```sh
1. Python 3.5
2. Django 1.11
3. MySQL
```

### Create Virtual Environment
Follow instructions at: *http://pypi.python.org/pypi/virtualenv*

### Install Requirements
```sh
pip install -r requirements/base.txt

```

### Run Migrations
```sh
python manage.py migrate
```

### Create Superuser
```sh
python manage.py createsuperuser
```

### Run Server
```sh
python manage.py runserver
```
