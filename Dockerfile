FROM python:3.10.8

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]