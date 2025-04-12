
FROM php:8.2-apache

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y     wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev     libssl-dev libreadline-dev libffi-dev libsqlite3-dev curl     libpq-dev ffmpeg libsm6 libxext6     cmake libboost-all-dev libopenblas-dev liblapack-dev unzip     && wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tgz &&     tar -xvf Python-3.9.18.tgz && cd Python-3.9.18 &&     ./configure --enable-optimizations && make -j$(nproc) && make altinstall &&     ln -sf /usr/local/bin/python3.9 /usr/bin/python3 &&     ln -sf /usr/local/bin/pip3.9 /usr/bin/pip3 &&     cd .. && rm -rf Python-3.9.18*

RUN docker-php-ext-install pdo pdo_pgsql

RUN pip3 install --upgrade pip --break-system-packages &&     pip3 install dlib==19.24.0 --break-system-packages &&     pip3 install face_recognition --break-system-packages &&     pip3 install flask flask_sqlalchemy flask_migrate psycopg2-binary opencv-python bcrypt gunicorn python-dotenv --break-system-packages

COPY php/ /var/www/html/
COPY app /app
COPY db.py /app/db.py
COPY .env /app/.env

WORKDIR /app

EXPOSE 80 5000

CMD service apache2 start && gunicorn -b 0.0.0.0:5000 app:create_app()
