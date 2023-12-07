### APP NAPPSTORE
*ECommerce - NappStore*

---------------
Web app dockerized | Django & Django Rest Framework

---------------

## Installation guide ⚙️
```
docker-compose up
```
---------------

## Access Web 🔗
```
http://127.0.0.1:8000
```
## Access Admin 🔗
Open in parallel terminal to enter the container
```
docker exec -it <IDCONTAINER> bash
$ python3 manage.py createsuperuser
```
```
http://127.0.0.1:8000/admin
```
## Endpoints
ENDPOINTS
```
http://localhost:8000/category - GET List / Post
http://localhost:8000/product - GET List / Post
http://localhost:8000/product/<id> - GET Detail
http://localhost:8000/product/<id>/update - UPDATE
http://localhost:8000/product/<id>/delete - DELETE
http://localhost:8000/carts - GET List / Post
http://localhost:8000/carts/<id> - GET Detail
http://localhost:8000/carts/<id>/update - UPDATE
```


---------------

## Application built with 🛠️

* [Python 3.7](https://www.python.org/) - Programming language
* [Django](https://www.djangoproject.com/) - Framework
* [Django Rest Framework](https://www.django-rest-framework.org/) - API REST
* [Docker](https://www.docker.com/) - Application deployment

---------------
## Developer ⌨️

* **Jesús Villegas** | [e-mail](jvncode@gmail.com)  |  [LinkedIn](https://www.linkedin.com/in/jes%C3%BAs-villegas-609b71198)


