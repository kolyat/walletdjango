# Copyright (c) 2021 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

from django import urls

from rest_framework_nested import routers

from . import views


wallet_router = routers.SimpleRouter()
wallet_router.register('wallet', views.UserWalletViewSet)

transaction_router = routers.NestedSimpleRouter(wallet_router, 'wallet',
                                                lookup='wallet')
transaction_router.register('transaction', views.MoneyTransactionViewSet,
                            basename='wallet-transaction')


urlpatterns = [
    urls.path('', views.IndexPage.as_view(), name='index'),

    # APIs
    urls.path('api/', urls.include(wallet_router.urls)),
    urls.path('api/', urls.include(transaction_router.urls)),
    urls.path('api/transactions/',
              views.MoneyTransactionsView.as_view({'get': 'list'}))
]
