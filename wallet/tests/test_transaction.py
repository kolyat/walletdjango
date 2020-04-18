# Copyright (c) 2020 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

import logging
import copy
import pytest

from testutils import rndutils
from wallet.management.commands import populate_db_wallet
from . import data_test_transaction


def post_transaction_path(wallet_pk):
    return f'/api/wallet/{wallet_pk}/transaction/'


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
        ({'comments': ''}, 201)
    ]
)
def test_transaction_field(db, client, field, expected_code):
    _pk = populate_db_wallet.add_wallet(__file__)
    _path = post_transaction_path(_pk)
    _data = copy.deepcopy(data_test_transaction.valid_transaction)
    _data.update(field)
    logging.info(f'POST {_path}: {_data}')
    response = client.post(_path, data=_data)
    logging.info(f'Status code: {response.status_code}')
    logging.info(response.json())
    assert response.status_code == expected_code
    assert data_test_transaction.validate_transaction(response.json())
    if response.status_code < 300:
        assert response.json() == _data
