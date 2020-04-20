# Copyright (c) 2020 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

import datetime
import decimal

from django.core import exceptions
from django.db import models

from walletdjango import settings


decimal.getcontext().prec = settings.WALLET_MAX_DIGITS+2
decimal.getcontext().rounding = decimal.ROUND_05UP

insufficient_funds = exceptions.ValidationError(
    message='Operation with transaction rejected: '
            'cannot decrease wallet balance below zero',
    code='insufficient_funds'
)


def new_wallet_name():
    """Generate name of a wallet using timestamp with microsecond precision

    :return: string with generated name
    """
    now = datetime.datetime.now()
    ts = str(int(now.timestamp() * 100000))
    return f'wallet-{ts}'


class UserWallet(models.Model):
    """Represents user's wallet
    """
    name = models.CharField(
        null=False, blank=False, unique=True, max_length=254,
        default=new_wallet_name(), editable=True, verbose_name='Name'
    )
    balance = models.DecimalField(
        null=False, blank=False, unique=False,
        max_digits=settings.WALLET_MAX_DIGITS+2, decimal_places=2,
        default=decimal.Decimal('0.00'),
        editable=False, verbose_name='Balance'
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class MoneyTransaction(models.Model):
    """Represents money transaction
    """
    wallet = models.ForeignKey(
        UserWallet, on_delete=models.CASCADE, related_name='money_transactions'
    )
    created = models.DateTimeField(
        null=False, blank=True, unique=False,
        auto_now_add=True, editable=False, verbose_name='Created'
    )
    amount = models.DecimalField(
        null=False, blank=False, unique=False,
        max_digits=settings.TRANSACTION_MAX_DIGITS+2, decimal_places=2,
        editable=True, verbose_name='Amount'
    )
    comments = models.TextField(
        null=True, blank=True, unique=False, max_length=254,
        editable=True, verbose_name='Comments'
    )

    def __str__(self):
        return f'{str(self.wallet)} {str(self.amount)} at {str(self.created)}'

    def __unicode__(self):
        return f'{str(self.wallet)} {str(self.amount)} at {str(self.created)}'

    def save(self, *args, **kwargs):
        """Override save() method to prevent decreasing wallet's balance
        below zero

        :return: None - on error, amount - on success
        """
        if (self.amount < 0) and (abs(self.amount) > self.wallet.balance):
            raise insufficient_funds
        super().save(*args, **kwargs)
        self.wallet.balance += self.amount
        self.wallet.save()

    def delete(self, *args, **kwargs):
        """Override delete() method to prevent decreasing wallet's balance
        below zero

        :return: None - on error, amount - on success
        """
        if (self.amount > 0) and (self.amount > self.wallet.balance):
            raise insufficient_funds
        super().delete(*args, **kwargs)
        self.wallet.balance -= self.amount
        self.wallet.save()

    class Meta:
        ordering = ('-created',)
