# summy
Simple text summarization written using Flask, spaCy and scikit-learn.
Application gets large English text and creates summarization using extractive approach.

## About

Microservice has two endpoints:
* `POST /document`
* `GET /document/<document_id>`

### `POST /document`

Accepts `application/x-www-form-urlencoded` request with text stored under `text` key.
Returns `application/json` response with document ID which can be used in the next endpoint.

### `GET /document/<document_id>`

Gets document ID as a parameter in the endpoint.
Returns `application/json` response with summarization created for the text stored under provided document ID.

## Requirements

Project was built using Python 3.6 and below technologies:
- [flask](https://flask.palletsprojects.com/)
- [flask-migrate](https://flask-migrate.readthedocs.io/)
- [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [scikit-learn](https://scikit-learn.org/)
- [spacy](https://spacy.io/)

## Getting Started

### Install Requirements

Install all above requirements using `Pipfile`:
```
$ pipenv install
$ pipenv shell
```

or `requirements.txt` file:
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Additionally download spaCy model `en_core_web_sm`:
```
$ python -m spacy download en_core_web_sm
```

### Initialize Database

Create database to keep summarizations:
```
$ flask db upgrade
```

### Run Server

After all, run server with default hostname (localhost) and port (5000):
```
$ flask run
```

## Usage

Use cUrl (or another tool) to call both endpoints:

### `POST /document`

```
$ curl -i -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "text=<put_your_text_here>"  http://localhost:5000/document

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 18
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Thu, 04 Nov 2021 02:56:11 GMT

{"document_id": 1}
```

### `GET /document/<document_id>`

```
$ curl -i http://localhost:5000/document/1

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 456
Server: Werkzeug/2.0.2 Python/3.9.7
Date: Thu, 04 Nov 2021 02:57:12 GMT

{"document_id": 1, "summary": "<summarization_of_provided_text>"}
```