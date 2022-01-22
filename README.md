# muimui_backend
## Our system architecture
![system architecture](https://i.postimg.cc/76Fcc59y/muimui.png)
## Other codes
- [muimui-frontend](https://github.com/GinGerBread-Yellow/muimui-frontend/)
- [muimui_backend](https://github.com/TimChou-ntu/muimui_backend/)
- [muimui_car](https://github.com/TintinWuNTUEE/muimui_car/)

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
# follow the prompts and create the user
```
- Run the backend server
```bash
$ python3 manage.py runserver 0.0.0.0:8000
```
- Run the backend server in ssl
```bash
$ python3 manage.py runsslserver
```
- You can access backend by input `http://localhost:8000/hide/` in your browser
## REST API format

### Auth
- login
    - `POST http://localhost:8000/api/token/`
    - `data: {"username", "password"}`

### view cars (AuthOnly)
- view all cars
    - `GET http://localhost:8000/rest/clients/`
- reserve a car
    - `POST http://localhost:8000/rest/clients/`
    - `data={"carID"}`

### connect to car
- get sdp, ip, carID
    - `GET http://localhost:8000/rest/cars/<YOUR_TOKEN>/`
- send your sdp answer
    - `POST http://localhost:8000/rest/cars/`
    - `data={"carID", "sdp", "carIP"}`

## Websocket connection
- to construct a websocket connection
    - `ws:/localhost:8000/ws/chat/`


