# Copyright (c) 2021 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

from django.contrib import admin

from . import models


@admin.register(models.UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')


@admin.register(models.MoneyTransaction)
class MoneyTransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'created', 'amount', 'comments')
    search_fields = ('wallet', 'created', 'amount', 'comments')
    ordering = ('-created',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
