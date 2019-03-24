**Olx rem**

writen with Python 3.7

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

