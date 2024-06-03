# Card Scheme API

## Description
This project provides a REST API service to retrieve information about credit card schemes.

## Endpoints
- `/api/card-scheme/verify/<card-number>`
- `/api/card-scheme/stats?start=<start>&limit=<limit>`

## Setup

### Using Virtual Environment
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=src/app.py
flask run