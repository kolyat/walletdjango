# Copyright (c) 2022 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

from rest_framework import serializers

from . import models


class UserWalletSerializerCU(serializers.ModelSerializer):
    """UserWallet model serializer for create/update procedures
    """
    class Meta:
        model = models.UserWallet
        fields = ['name']


class UserWalletSerializerR(serializers.ModelSerializer):
    """UserWallet model serializer for data retrieval
    """
    class Meta:
        model = models.UserWallet
        fields = '__all__'
        read_only_fields = ['name', 'balance']


class MoneyTransactionSerializerC(serializers.ModelSerializer):
    """MoneyTransaction model serializer for create procedure
    """
    class Meta:
        model = models.MoneyTransaction
        fields = ['wallet', 'amount', 'comments']


class MoneyTransactionSerializerR(serializers.ModelSerializer):
    """MoneyTransaction model serializer for data retrieval
    """
    class Meta:
        model = models.MoneyTransaction
        fields = '__all__'
        read_only_fields = ['wallet', 'created', 'amount', 'comments']

