# walletdjango

Very simple electronic wallet with money transaction support. Implemented as a 
REST-service within the test task.

## API description

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
