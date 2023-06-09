FROM python:3.11.1-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src  /code/src


CMD ["uvicorn", "src.main:app", "--reload","--host", "0.0.0.0", "--port", "80", "--workers", "4"]