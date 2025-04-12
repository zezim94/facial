
FROM php:8.2-apache

RUN apt-get update && apt-get install -y python3 python3-pip ffmpeg libsm6 libxext6 curl \
    && docker-php-ext-install pdo pdo_pgsql

COPY php/ /var/www/html/
COPY . /srv/app/
WORKDIR /srv/app

RUN pip3 install flask flask_sqlalchemy flask_migrate psycopg2-binary face_recognition opencv-python bcrypt gunicorn

EXPOSE 80 5000

CMD service apache2 start && gunicorn -b 0.0.0.0:5000 app:create_app()
