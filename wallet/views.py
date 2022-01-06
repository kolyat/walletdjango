# Copyright (c) 2022 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

import os

from django import views

from rest_framework import viewsets, mixins

from walletdjango import settings
from . import models, serializers


class MultipleSerializerGenericViewSet(viewsets.GenericViewSet):
    """Extension of GenericViewSet that supports multiple serializers for each
    action. Dictionary with 'action-serializer' pair is stored in 'serializers'
    property:

    serializers = {
        'create': CreateUpdateSerializer,
        'retrieve': RetrieveSerializer,
        ...
    }

    Overrides get_serializer_class(), returns defined serializer based on
    current action. If serializer is not found, returns 'serializer_class' as a
    default.
    """
    serializers = {}

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializer_class)


class IndexPage(views.generic.TemplateView):
    """Index page with API description
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        markdowntext = open(
            os.path.join(settings.BASE_DIR, 'README.md')).read()
        context = super().get_context_data(**kwargs)
        context['markdowntext'] = markdowntext
        return context


class UserWalletViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        MultipleSerializerGenericViewSet):
    queryset = models.UserWallet.objects.all()
    serializer_class = serializers.UserWalletSerializerCU
    serializers = {
        'create': serializers.UserWalletSerializerCU,
        'retrieve': serializers.UserWalletSerializerR,
        'update':  serializers.UserWalletSerializerCU,
        'list': serializers.UserWalletSerializerR
    }


class MoneyTransactionViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              MultipleSerializerGenericViewSet):
    serializer_class = serializers.MoneyTransactionSerializerR
    serializers = {
        'create': serializers.MoneyTransactionSerializerC,
        'retrieve': serializers.MoneyTransactionSerializerR,
        'list': serializers.MoneyTransactionSerializerR
    }

    def get_queryset(self):
        return models.MoneyTransaction.objects.filter(
            wallet=self.kwargs['wallet_pk'])


class MoneyTransactionsView(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = models.MoneyTransaction.objects.all()
    serializer_class = serializers.MoneyTransactionSerializerR
