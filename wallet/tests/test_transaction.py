# Copyright (c) 2020 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

import os
import logging
import copy
import pytest

from django.core import exceptions

from testutils import rndutils, apiutils
from wallet.management.commands import populate_db_wallet
from . import data_test_transaction


@pytest.mark.parametrize(
    'field, expected_code',
    [
        ({'wallet': 1}, 201),
        ({'wallet': -1}, 400),
        ({'wallet': 0}, 400),
        ({'wallet': 0.44}, 400),
        ({'wallet': 999}, 400),
        ({'wallet': 'abc'}, 400),
        ({'comments': 'NEW COMMENTS'}, 201),
        ({'comments': rndutils.random_str(253)}, 201),
        ({'comments': rndutils.random_numstr(254)}, 201),
        ({'comments': rndutils.random_numstr(255)}, 400),
        ({'comments': ''}, 201),
        ({'amount': '12345.67'}, 201),
        ({'amount': '-100000'}, 400),
        ({'amount': '100000'}, 400),
        ({'amount': ''}, 400),
        ({'amount': 'abc'}, 400),
        ({'amount': '0.123'}, 400),
    ]
)
def test_transaction_field(db, client, field, expected_code):
    """Test field validation within creating money transaction

    :param db: database access fixture
    :param client: Django client fixture
    :param field: field under testing
    :param expected_code: expected response code
    """
    _pk = populate_db_wallet.add_wallet(os.path.basename(__file__))
    _path = apiutils.create_transaction_path(_pk)
    _data = copy.deepcopy(data_test_transaction.valid_transaction)
    _data.update(field)
    response = apiutils.post(db, client, _path, _data)
    assert response.status_code == expected_code
    assert data_test_transaction.validate_transaction(response.json())
    if response.status_code < 300:
        assert response.json() == _data


@pytest.mark.parametrize(
    'remove_field, expected_code',
    [
        ('wallet', 400),
        ('amount', 400),
        ('comments', 201),
    ]
)
def test_transaction_partial(db, client, remove_field, expected_code):
    """Test transaction with partial payload

    :param db: database access fixture
    :param client: Django client fixture
    :param remove_field: field to remove from payload template
    :param expected_code: expected response code
    """
    _pk = populate_db_wallet.add_wallet(os.path.basename(__file__))
    _path = apiutils.create_transaction_path(_pk)
    _data = copy.deepcopy(data_test_transaction.valid_transaction)
    _data.pop(remove_field)
    response = apiutils.post(db, client, _path, _data)
    assert response.status_code == expected_code


@pytest.mark.xfail(
    raises=exceptions.ValidationError,
    reason='Unhandled exception in case decreasing balance below zero '
           'or increasing above maximum'
)
def test_transaction_amount_and_wallet_balance(db, client):
    """Test transaction amount and wallet balance

    :param db: database access fixture
    :param client: Django client fixture
    """
    _pk = populate_db_wallet.add_wallet(os.path.basename(__file__))
    get_wallet_path = apiutils.get_wallet_path(_pk)
    post_transaction_path = apiutils.create_transaction_path(_pk)
    _data = copy.deepcopy(data_test_transaction.valid_transaction)

    _data.update({'amount': '99999.99'})
    response = apiutils.post(db, client,
                             post_transaction_path, _data)
    assert response.json()['amount'] == '99999.99'
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '99999.99'
    apiutils.post(db, client, post_transaction_path, _data)
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '199999.98'

    _data.update({'amount': '-99999.99'})
    response = apiutils.post(db, client,
                             post_transaction_path, _data)
    assert response.json()['amount'] == '-99999.99'
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '99999.99'
    apiutils.post(db, client, post_transaction_path, _data)
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '0.00'

    _data.update({'amount': '0.01'})
    response = apiutils.post(db, client,
                             post_transaction_path, _data)
    assert response.json()['amount'] == '0.01'
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '0.01'

    _data.update({'amount': '-0.01'})
    response = apiutils.post(db, client,
                             post_transaction_path, _data)
    assert response.json()['amount'] == '-0.01'
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '0.00'

    # TODO: handle decreasing balance below zero
    response = apiutils.post(db, client,
                             post_transaction_path, _data)
    # TODO: assert server response
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '0.00'

    _data.update({'amount': '0.00'})
    response = apiutils.post(db, client,
                             post_transaction_path, _data)
    assert response.json()['amount'] == '0.00'
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '0.00'

    _data.update({'amount': '99999.99'})
    for _ in range(10):
        apiutils.post(db, client, post_transaction_path, _data)
    _data.update({'amount': '0.09'})
    apiutils.post(db, client, post_transaction_path, _data)
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '999999.99'
    _data.update({'amount': '0.01'})
    # TODO: handle increasing balance above maximum
    response = apiutils.post(db, client,
                             post_transaction_path, _data)
    # TODO: assert server response
    response = apiutils.get(db, client, get_wallet_path)
    logging.info(f'Wallet {_pk} balance: {response.json()["balance"]}')
    assert response.json()['balance'] == '999999.99'
