# Copyright (c) 2020 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

import pytest

from testutils import rndutils, apiutils
from . import data_test_wallet


@pytest.mark.parametrize(
    'payload, expected_code',
    [
        ({'name': 'NEW WALLET'}, 201),
        ({'name': rndutils.random_str(253)}, 201),
        ({'name': rndutils.random_numstr(254)}, 201),
        ({'name': rndutils.random_numstr(255)}, 400),
        ({'name': ''}, 201),
        ({}, 201),
        # TODO: implements as separate test
        # ({'name': 'wallet with balance', 'balance': '100.00'}, 201)
    ]
)
def test_create_wallet(db, client, payload, expected_code):
    """Test wallet create

    :param db: database access fixture
    :param client: Django client fixture
    :param payload: testing payload
    :param expected_code: expected response code
    """
    _path = apiutils.create_wallet_path()
    response = apiutils.post(db, client, _path, payload)
    assert response.status_code == expected_code
    assert data_test_wallet.validate_wallet(response.json())
