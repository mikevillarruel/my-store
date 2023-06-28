FROM python:3.10

WORKDIR /project

COPY .  /project

RUN pip install --no-cache-dir -r /project/requirements.txt

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
