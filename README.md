# Egyptian National Id Validators

## Installation
1. Clone repository on your machine
2. Go in IDValidator/idvalidator directory
3. Run cmd 
```bash
python3 manage.py runserver
```
4. Now API is running on localhost:8000

## Validating ID 
1. Checking if id number is more or less than 14 numbers
2. Checking first number is 2 or 3 
3. Checking next 6 numbers are a valid birthdate 
I chose here to check using the below code for simplicity. If detailed validation was needed, could have checked day, month and year indivually and returned the corrseponding error.

```python
dateObject = datetime.strptime(birthDate,'%d/%m/%Y')
```

## Extracting information
Extracted birthdate using first 7 numbers, and city code, any more information in the ID number can be extracted same way 

## Rate limiting 

```python
@ratelimit(key='user_or_ip', rate='10/m')
```
## Authentication 
Used JWT for authentication. 

To get token, call POST request below

```http
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json
Authorization: Basic YWRtaW46YWRtaW4=
{
    "username":"admin",
    "password":"admin"
}
```

To test jwt authentication, call POST request below. Use token from previous request

```http
POST http://127.0.0.1:8000/api/validator
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2NTQzNDI5LCJpYXQiOjE3MzY1NDMxMjksImp0aSI6ImQ3MmQyOGQwZjg1OTQ5ZmRhMjViNmI4YjQxYjhkMmVmIiwidXNlcl9pZCI6MX0.udv_QRuRVARBd_wQeJHmQrLixQQEkOZTYf548kncibM
{
    "number":"28903170200808"
}
```

For simplicity, all other test cases use basic authentication. 

## Tracking Calls 

Thinking of a free way to achieve this other than google analytics or moesif, I created a table in the database to store number of visits per user. 

When validator is visited, the program checks if the user of the request has a record in the api_visit table, if so it will increment the visit count if not it will create a new record for the user with visit count =1 

1. Call validator as user: admin as much times as needed
```http
POST http://127.0.0.1:8000/api/validator
Content-Type: application/json
Authorization: Basic YWRtaW46YWRtaW4=
{
    "number":"28903170200808"
}
```

2. Call validator as user: admin2 as much time as needed
```http
POST http://127.0.0.1:8000/api/validator
Content-Type: application/json
Authorization: Basic YWRtaW4yOmFkbWluMg==
{
    "number":"28903170200808"
}
```


3. Get API visits to check that number of visits per user has been updated accordingly
```http
GET  http://127.0.0.1:8000/api/visits
Content-Type: application/json
Authorization: Basic YWRtaW46YWRtaW4=
```


## Test Cases 
Extra test cases are in test.rest
