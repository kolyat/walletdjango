# Copyright (c) 2020 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

import logging


def get_wallet_path(wallet_pk):
    return f'/api/wallet/{wallet_pk}/'


def create_wallet_path():
    return f'/api/wallet/'


def create_transaction_path(wallet_pk):
    return f'/api/wallet/{wallet_pk}/transaction/'


def get(db, client, path):
    """Client GET wrapper

    :param db: database access fixture
    :param client: Django client fixture
    :param path: GET path

    :return: response object
    """
    logging.info(f'GET {path}')
    _response = client.get(path)
    logging.info(f'Status code: {_response.status_code}')
    logging.info(_response.json())
    return _response


def post(db, client, path, data):
    """Client POST wrapper

    :param db: database access fixture
    :param client: Django client fixture
    :param path: POST path
    :param data: payload

    :return: response object
    """
    logging.info(f'POST {path}: {data}')
    _response = client.post(path, data=data)
    logging.info(f'Status code: {_response.status_code}')
    logging.info(_response.json())
    return _response
