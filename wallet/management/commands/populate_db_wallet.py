# Copyright (c) 2021 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

import decimal

from django.core.management import base

from walletdjango import settings
from wallet import models

decimal.getcontext().prec = settings.WALLET_MAX_DIGITS+2
decimal.getcontext().rounding = decimal.ROUND_05UP


def add_wallet(name=models.new_wallet_name()):
    """Create new wallet

    :param name: name of a wallet

    :return: wallet's primary key
    """
    print('  {:.<42}...'.format(name), end='', flush=True)
    _wallet = models.UserWallet(name=name)
    _wallet.save()
    print(f'PK={_wallet.pk}')
    return _wallet.pk


def add_transaction(wallet_pk, amount, comments=''):
    """Add transaction to a wallet

    :param wallet_pk: primary key of a wallet
    :param amount: money amount
    :param comments: transaction comments

    :return: transaction's primary key
    """
    print('    {:.<45}'
          ''.format(f'Transaction {amount:+} to wallet {wallet_pk}...'),
          end='', flush=True)
    _wallet = models.UserWallet.objects.get(pk=wallet_pk)
    _transaction = models.MoneyTransaction(wallet=_wallet, amount=amount,
                                           comments=comments)
    _transaction.save()
    print(f'{_wallet.balance:.2f}')
    return _transaction.pk


def prepare_wallets():
    print('Create data for WALLET app:')
    add_wallet(name='empty_wallet')
    _pk = add_wallet(name='wallet-min')
    add_transaction(wallet_pk=_pk, amount=decimal.Decimal('0.01'))
    _pk = add_wallet(name='main_wallet')
    add_transaction(wallet_pk=_pk, amount=decimal.Decimal('101.99'))
    add_transaction(wallet_pk=_pk, amount=decimal.Decimal('-100.11'))
    _pk = add_wallet(name='wallet-max')
    for _ in range(10):
        add_transaction(wallet_pk=_pk, amount=decimal.Decimal('99999.99'))
    add_transaction(wallet_pk=_pk, amount=decimal.Decimal('0.09'))


class Command(base.BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        prepare_wallets()
