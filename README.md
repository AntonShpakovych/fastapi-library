# FastAPI Library


## Navigation
- [About project](#about-project)
- [Technologies](#technologies)
- [Installation](#installation)
<hr>

## About Project
    This is an API that provides the ability to view books or download them.
<hr>

## Technologies
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
- [Redis](https://redis.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [S3](https://aws.amazon.com/ru/s3/)


## Installation

```shell
    1) git clone https://github.com/AntonShpakovych/fastapi-library.git
    2) cd into project root
    3) create a .env file based on .env.sample
    4) docker compose up --build
```
<hr>


## What this project can do
This service can store book files on S3, extract a pdf file of a book or HTML, and accept a csv file that will indicate which book can only be obtained through HTML.