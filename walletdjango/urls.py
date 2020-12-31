# Copyright (c) 2021 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

from django.contrib import admin
from django import urls


urlpatterns = [
    urls.path('', urls.include('wallet.urls')),
    urls.path('admin/', admin.site.urls)
]
