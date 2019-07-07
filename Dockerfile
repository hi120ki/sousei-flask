FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

COPY ./app /app

RUN rm -f /app/app.db

RUN pip install flask_session
RUN pip install flask_sqlalchemy
RUN pip install flask-talisman
