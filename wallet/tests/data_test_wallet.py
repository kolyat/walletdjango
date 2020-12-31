# Copyright (c) 2021 Kirill 'Kolyat' Kiselnikov
# This file is the part of walletdjango, released under modified MIT license
# See the file LICENSE included in this distribution


import fastjsonschema


validate_wallet = fastjsonschema.compile({
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'definitions': {
        'wallet': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer', 'minimum': 1},
                'name': {'type': 'string'},
                'balance': {'type': 'string', 'pattern': '[0-9]+\.[0-9]{2}'}
            },
            'additionalProperties': False,
            'required': ['name'],
        }
    },
    'anyOf': [
        {'$ref': '#/definitions/wallet'},
        {
            'type': 'array',
            'minItems': 0,
            'uniqueItems': True,
            'items': {'$ref': '#/definitions/wallet'}
        },
        {
            'properties': {
                'name': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            }
        }
    ]
})
