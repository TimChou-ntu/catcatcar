# muimui_backend


## Env
- python 3.7.1
## How to run
- Install project dependencies
```bash
$ pip3 install -r requirements.txt
```
- Create .env and put your secret key in it
```bash
$ cd mysite/
$ echo SECRET_KEY={your secret} > .env
```
- Migrate database tables
```bash
$ python3 manage.py makemigration
$ python3 manage.py migrate
```
- Create super user
```bash
$ python3 manage.py createsuperuser
```
- Run the backend server
```bash
$ python3 manage.py runserver 0.0.0.0:8000
```
- Run the backend server in ssl
```bash
$ python3 manage.py runsslserver
```



## Using `curl` to perform client request
```bash
$ curl http://localhost:8000/rest/tutorial
```
Or you can use `http` to send request
```bash
$ sudo apt-get install httpie
$ http --json http://localhost:8000/rest/tutorial
```
