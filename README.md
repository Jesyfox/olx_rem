**Olx rem**

writen with Python 3.7

you will need:

**redis**

**postgresql**

Instalation:

virtualenv:
1. `python3 -m venv venv`
2. `. venv/bin/activate`
3. `pip install -r requirements.txt`

database:
1. `sudo su - postgres`
2. `psql`
3. `CREATE DATABASE olx_rem;`
4. `CREATE USER olx_db WITH PASSWORD '123456';`
5. `GRANT ALL PRIVILEGES ON DATABASE olx_rem TO olx_db;`
6. `ALTER USER olx_db CREATEDB;` for testing

You must be here: `*your folder*/olx_rem/olx_rem`

run migrations: `./manage.py migrate`

open 2 teminals:
at first terminal: `celery -A classified_ads worker --loglevel=info`
at second terminal: `./manage.py runserver`

First of all you need create a super user and add some categories through
admin page(dont fill slug form, it will fill automatically)
