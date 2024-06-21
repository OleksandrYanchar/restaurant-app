
## Installation

Clone this repository:

```bash
git clone git@github.com:OleksandrYanchar/restaurant-app.git
```
    
## Run  docker app:

```bash
docker-compose up --build
```
or 

```bash
make build
```
```bash
make run 
```

## Manualy run 

default app

```bash
python manage.py runserver
```

## run tests 

```bash
make test:
```
if throws error:
```bash
make test-restaurant
```

## manual run tests

```bash
python manage.py test
```

if throws error:
```bash
python manage.py test apps/restaurants/tests/
```

# Project Links

## Swagger
- [swagger](http://http://localhost/api/v1/swagger/)

## Check Database Data
- [adminer](http://localhost:8080)

## Django admin
- [admin panel](http://localhost/api/v1/admin/)
