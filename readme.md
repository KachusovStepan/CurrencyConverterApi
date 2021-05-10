# Currency converter REST API

Author: Kachusov Stepan

| Action        | Method           | Endpoint | Parameters |
| :------------- |:-------------| :-----| :--- |
| Convert an amount of money from one currency to another | GET | /convert | from, to, amount |
| Update exchange rates | POST | /database | merge |

<br>
If merge = 0, then the old data is invalidated;<br>
If merge = 1, then the new data overwrites the old, but the old is still relevant, if not overwritten.<br>
<br>

## Examples

### GET /convert?from=USD&to=EUR&amount=42
#### Responses:
```
{"status": "success", "amount": 38.791909115399996}
```
```
{"status": "failed", "message": "unknown currency names"}
```

## POST /database?merge=1
### body:
```
{
    'EUR': {
        'USD': 1.2411,
        'EUR': 1.0
    },
    'USD' : {
        'EUR': 0.9236168837,
        'USD': 1.0
    },
}
```
#### Response:
```
{"status": "success", "message": "successfuly updated"}
```

## Start API
```
docker-compose up
```