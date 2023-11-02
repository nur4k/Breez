FROM python:3.11-slim 
WORKDIR /app
## Install poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH=$PATH:/etc/poetry/bin

##
ADD ./poetry.lock ./pyproject.toml ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --only main

COPY . /app/

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]