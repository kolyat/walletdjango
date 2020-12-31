# walletdjango

Very simple electronic wallet with money transaction support. Implemented as a 
REST-service within the test task.

## API description


### Wallet

#### Create wallet

* **URL**:
`/api/wallet/`

* **Method**:
`POST`
  
* **URL parameters**:
`none`

* **Data parameters**:
    * Required:<br>
        `"name": string` - name of a wallet

* **Success response**
    * Code: `201 CREATED`

* **Error response**
    * Code: `400 BAD REQUEST`
        * `{"name": ["Ensure this field has no more than 254 characters."]}`
 
##### Sample call

Request:
`POST /api/wallet/`
```json
{
    "name": "Name of a wallet"
}
```
Response data:
```json
{
    "name": "Name of a wallet"
}
```

#### Update wallet

* **URL**:
`/api/wallet/<int:wallet_pk>/`

* **Method**:
`PUT`, `PATCH`
  
* **URL parameters**:
`none`

* **Data parameters**:
    * Required:<br>
        `"name": string` - name of a wallet

* **Success response**
    * Code: `200 OK`

* **Error response**
    * Code: `400 BAD REQUEST`
        * `{"name": ["Ensure this field has no more than 254 characters."]}`
 
##### Sample call

Request:
`PATCH /api/wallet/3/`
```json
{
    "name": "New name of a wallet"
}
```
Response data:
```json
{
    "name": "New name of a wallet"
}
```

#### Get wallet

Retrieve wallet status, name and balance.

* **URL**:
`/api/wallet/<int:wallet_pk>/`

* **Method**:
`GET`
  
* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`

* **Error response**
    * Code: `404 NOT FOUND`
 
##### Sample call

Request:
`GET /api/wallet/3/`

Response data:
```json
{
    "id": 3,
    "name": "main_wallet",
    "balance": "1.88"
}
```

#### List wallets

Retrieve list of all wallets.

* **URL**:
`/api/wallet/`

* **Method**:
`GET`
  
* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`

* **Error response**
`none`
 
##### Sample call

Request:
`GET /api/wallet/`

Response data:
```json
[
    {
        "id": 1,
        "name": "empty_wallet",
        "balance": "0.00"
    },
    {
        "id": 3,
        "name": "main_wallet",
        "balance": "1.88"
    },
    {
        "id": 5,
        "name": "123",
        "balance": "100.15"
    }
]
```

#### Delete wallet

* **URL**:
`/api/wallet/<int:wallet_pk>/`

* **Method**:
`DELETE`
  
* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `204 NO CONTENT`

* **Error response**
    * Code: `404 NOT FOUND`
 
##### Sample call

Request:
`DELETE /api/wallet/3/transaction/3/`


### Transactions

#### Create transaction

* **URL**:
`/api/wallet/<int:wallet_pk>/transaction/`

* **Method**:
`POST`
  
* **URL parameters**:
`none`

* **Data parameters**:
    * Required:<br>
        `"wallet": integer` - primary key of a wallet<br>
        `"amount": string` - decimal as a string: `[0-9]+.[0-9]{2}`
                             (e. g., "100.15")<br>
    * Optional:<br>
        `"comments": string` - description of a money transaction<br>

* **Success response**
    * Code: `201 CREATED`

* **Error response**
    * Code: `400 BAD REQUEST`
        * `{"wallet": ["Invalid pk "0" - object does not exist."]}`
        * `{"wallet": ["Incorrect type. Expected pk value, received str."]}`
        * `{"comments": ["Ensure this field has no more than 254 characters."]}`
 
##### Sample call

Request:
`POST /api/wallet/1/transaction/`
```json
{
    "wallet": 1,
    "amount": "100.15",
    "comments": "Some comments here"
}
```
Response data:
```json
{
    "wallet": 1,
    "amount": "100.15",
    "comments": "Some comments here"
}
```

#### Get transaction

Retrieve info about specified transaction.

* **URL**:
`/api/wallet/<int:wallet_pk>/transaction/<int:transaction_pk>/`

* **Method**:
`GET`
  
* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`

* **Error response**
    * Code: `404 NOT FOUND`
 
##### Sample call

Request:
`GET /api/wallet/3/transaction/3/`

Response data:
```json
{
    "id": 3,
    "created": "2021-04-19T13:30:59.438048Z",
    "amount": "-100.11",
    "comments": "",
    "wallet": 3
}
```

#### List transactions (wallet)

List all transactions of specified wallet.

* **URL**:
`/api/wallet/<int:wallet_pk>/transaction/`

* **Method**:
`GET`
  
* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`

* **Error response**
`none`
 
##### Sample call

Request:
`GET /api/wallet/3/transaction/`

Response data:
```json
[
    {
        "id": 3,
        "created": "2021-04-19T13:30:59.438048Z",
        "amount": "-100.11",
        "comments": "",
        "wallet": 3
    },
    {
        "id": 2,
        "created": "2021-04-19T13:30:59.422448Z",
        "amount": "101.99",
        "comments": "",
        "wallet": 3
    }
]
```

#### List all transactions

Retrieve full transaction list of all wallets.

* **URL**:
`/api/transactions/`

* **Method**:
`GET`
  
* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `200 OK`

* **Error response**
`none`
 
##### Sample call

Request:
`GET /api/transactions/`

Response data:
```json
[
    {
        "id": 14,
        "created": "2021-04-19T13:30:59.672048Z",
        "amount": "0.09",
        "comments": "",
        "wallet": 4
    },
    {
        "id": 4,
        "created": "2021-04-19T13:30:59.469248Z",
        "amount": "99999.99",
        "comments": "",
        "wallet": 4
    },
    {
        "id": 3,
        "created": "2021-04-19T13:30:59.438048Z",
        "amount": "-100.11",
        "comments": "",
        "wallet": 3
    },
    {
        "id": 2,
        "created": "2021-04-19T13:30:59.422448Z",
        "amount": "101.99",
        "comments": "",
        "wallet": 3
    },
    {
        "id": 1,
        "created": "2021-04-19T13:30:59.391248Z",
        "amount": "0.01",
        "comments": "",
        "wallet": 2
    }
]
```

#### Delete transaction

* **URL**:
`/api/wallet/<int:wallet_pk>/transaction/<int:transaction_pk>/`

* **Method**:
`DELETE`
  
* **URL parameters**:
`none`

* **Data parameters**:
`none`

* **Success response**
    * Code: `204 NO CONTENT`

* **Error response**
    * Code: `404 NOT FOUND`
 
##### Sample call

Request:
`DELETE /api/wallet/3/transaction/3/`
