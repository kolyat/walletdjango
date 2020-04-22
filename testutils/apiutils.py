# Copyright (c) 2020 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution

import logging


def create_wallet_path():
    return f'/api/wallet/'


def put_patch_wallet_path(wallet_pk):
    return f'/api/wallet/{wallet_pk}/'


def get_wallet_path(wallet_pk):
    return f'/api/wallet/{wallet_pk}/'


def list_wallets_path():
    return f'/api/wallet/'


def delete_wallet_path(wallet_pk):
    return f'/api/wallet/{wallet_pk}/'


def create_transaction_path(wallet_pk):
    return f'/api/wallet/{wallet_pk}/transaction/'


def get_transaction_path(wallet_pk, transaction_pk):
    return f'/api/wallet/{wallet_pk}/transaction/{transaction_pk}/'


def list_wallet_transactions_path(wallet_pk):
    return f'/api/wallet/{wallet_pk}/transaction/'


def list_all_transactions_path():
    return f'/api/transactions/'


def delete_transaction_path(wallet_pk, transaction_pk):
    return f'/api/wallet/{wallet_pk}/transaction/{transaction_pk}/'


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


def put(db, drf_client, path, data):
    """Client PUT wrapper

    :param db: database access fixture
    :param drf_client: Django Rest Framework client fixture
    :param path: PUT path
    :param data: payload

    :return: response object
    """
    logging.info(f'PUT {path}: {data}')
    _response = drf_client.put(path, data=data)
    logging.info(f'Status code: {_response.status_code}')
    logging.info(_response.json())
    return _response


def patch(db, drf_client, path, data):
    """Client PATCH wrapper

    :param db: database access fixture
    :param drf_client: Django Rest Framework client fixture
    :param path: PATCH path
    :param data: payload

    :return: response object
    """
    logging.info(f'PATCH {path}: {data}')
    _response = drf_client.patch(path, data=data)
    logging.info(f'Status code: {_response.status_code}')
    logging.info(_response.json())
    return _response


def delete(db, client, path):
    """Client DELETE wrapper

    :param db: database access fixture
    :param client: Django client fixture
    :param path: DELETE path

    :return: response object
    """
    logging.info(f'DELETE {path}')
    _response = client.delete(path)
    logging.info(f'Status code: {_response.status_code}')
    try:
        logging.info(_response.json())
    except TypeError:
        logging.info('No response body')
    return _response
