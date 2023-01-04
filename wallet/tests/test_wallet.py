# Copyright (c) 2023 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

import decimal
import pytest

from testutils import rndutils, apiutils
from wallet.management.commands import populate_db_wallet
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


def test_retrieve_wallet(db, client):
    """Try to create wallet with defined balance, retrieve wallet's status

    :param db: database access fixture
    :param client: Django client fixture
    """
    _path = apiutils.create_wallet_path()
    response = apiutils.post(
        db, client, _path,
        {'name': 'wallet with balance', 'balance': '100.00'}
    )
    assert response.status_code == 201
    w_path = apiutils.get_wallet_path(wallet_pk=1)
    response = apiutils.get(db, client, w_path)
    assert response.status_code == 200
    assert data_test_wallet.validate_wallet(response.json())
    assert response.json()['balance'] == '0.00'


@pytest.mark.parametrize(
    'payload, expected_code, expected_name',
    [
        ({'name': 'UPDATED WALLET'}, 200, 'UPDATED WALLET'),
        ({'name': '1'*253}, 200, '1'*253),
        ({'name': '2'*254}, 200, '2'*254),
        ({'name': '3'*255}, 400, None),
        ({'name': ''}, 200, 'test wallet'),
        ({}, 200, 'test wallet'),
    ]
)
def test_update_wallet(db, drf_client, payload, expected_code, expected_name):
    """Test wallet update via PUT

    :param db: database access fixture
    :param drf_client: Django Rest Framework client fixture
    :param payload: testing payload
    :param expected_code: expected response code
    :param expected_name: expected wallet's name after changes
    """
    w_pk = populate_db_wallet.add_wallet('test wallet')
    _path = apiutils.put_patch_wallet_path(w_pk)
    response = apiutils.put(db, drf_client, _path, payload)
    assert response.status_code == expected_code
    assert data_test_wallet.validate_wallet(response.json())
    if response.status_code < 300:
        assert response.json()['name'] == expected_name


def test_update_wallet_with_balance(db, drf_client):
    """Try to update wallet via PATCH with defined balance in payload, retrieve
    wallet's status

    :param db: database access fixture
    :param drf_client: Django Rest Framework client fixture
    """
    w_pk = populate_db_wallet.add_wallet('Wallet')
    _path = apiutils.put_patch_wallet_path(w_pk)
    response = apiutils.patch(
        db, drf_client, _path,
        {'name': 'wallet with balance 2', 'balance': '100.00'}
    )
    assert response.status_code == 200
    w_path = apiutils.get_wallet_path(wallet_pk=w_pk)
    response = apiutils.get(db, drf_client, w_path)
    assert response.status_code == 200
    assert data_test_wallet.validate_wallet(response.json())
    assert response.json()['balance'] == '0.00'


def test_list_wallets(db, client):
    """List all wallets

    :param db: database access fixture
    :param client: Django client fixture
    """
    for i in (1, 2, 3, 4, 5):
        populate_db_wallet.add_wallet(f'wallet-{i}')
    _path = apiutils.list_wallets_path()
    response = apiutils.get(db, client, _path)
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_delete_wallet(db, client):
    """Test wallet deletion

    :param db: database access fixture
    :param client: Django client fixture
    """
    w_pk = populate_db_wallet.add_wallet()
    for _ in (1, 2, 3):
        populate_db_wallet.add_transaction(
            w_pk,
            decimal.Decimal('123.11')
        )
    _path = apiutils.delete_wallet_path(w_pk)
    response = apiutils.delete(db, client, _path)
    assert response.status_code == 204
    response = apiutils.get(db, client, _path)
    assert response.status_code == 404
