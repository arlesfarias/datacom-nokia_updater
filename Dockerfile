FROM python:3.10.8

COPY . /app

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip\
    && pip install -r requirements.txt

CMD ["gunicorn", "app:app", "-w", "3", "-b", "0.0.0.0:8000"]