from django.contrib.auth.models import User
from django.db import models

from src.constants import CURRENCY_CHOICES, RUPEES


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BankAccount(BaseModel):
    user = models.OneToOneField(User, related_name='accounts', on_delete=models.CASCADE)
    account_number = models.CharField(unique=True, max_length=100)
    balance = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)
    currency = models.CharField(choices=CURRENCY_CHOICES, blank=True, null=True, default=RUPEES, max_length=30)
    first_name = models.CharField(max_length=130, blank=True, null=True)
    last_name = models.CharField(max_length=130, blank=True, null=True)

    class Meta:
        db_table = 'bank_accounts'

    def __str__(self):
        return self.account_number

    def save(self, *args, **kwargs):
        if not self.account_number:
            from .utils import generate_unique_id
            self.account_number = generate_unique_id()
        super().save(*args, **kwargs)


class Transaction(BaseModel):
    reference_number = models.CharField(max_length=100, unique=True)
    debit_account = models.CharField(null=True, blank=True, max_length=100)
    credit_account = models.CharField(null=True, blank=True, max_length=100)
    amount = models.DecimalField(default=0.0, max_digits=12, decimal_places=2)
    is_successful = models.BooleanField(default=False)

    class Meta:
        db_table = 'bank_transactions'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return self.reference_number

    def save(self, *args, **kwargs):
        if not self.reference_number:
            from .utils import generate_unique_id
            self.reference_number = generate_unique_id()
        super().save(*args, **kwargs)
