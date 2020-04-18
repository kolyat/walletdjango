# Copyright (c) 2020 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution


import fastjsonschema


validate_transaction = fastjsonschema.compile({
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'definitions': {
        'transaction': {
            'type': 'object',
            'properties': {
                'wallet': {'type': 'integer', 'minimum': 0},
                'amount': {'type': 'string', 'pattern': '[0-9]+\.[0-9]{2}'},
                'comments': {'type': 'string'}
            },
            'additionalProperties': False,
            'required': ['wallet', 'amount', 'comments'],
        }
    },
    'anyOf': [
        {'$ref': '#/definitions/transaction'},
        {
            'properties': {
                'wallet': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            }
        },
        {
            'properties': {
                'comments': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            }
        },
    ]
})

valid_transaction = {
    'wallet': 1,
    'amount': '1.00',
    'comments': 'some comments here'
}
