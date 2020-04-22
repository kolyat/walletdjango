# Copyright (c) 2020 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

from rest_framework import test
import pytest


@pytest.fixture
def drf_client():
    """:return: Django Rest Framework client object
    """
    return test.APIClient()
