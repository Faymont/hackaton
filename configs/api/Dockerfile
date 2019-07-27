FROM python:slim-stretch

ARG uid=1000
ARG username=user
ARG environment
ARG project_name
ENV LANG=ru_RU.UTF-8 LC_ALL=ru_RU.UTF-8 LANGUAGE=ru_RU.UTF-8
ENV PYTHONBUFFERED=1 TERM=xterm-256color DEBIAN_FRONTEND=noninteractive PROJECT_NAME=${project_name}

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen && \
    echo "LANG=ru_RU.UTF-8" > /etc/default/locale && \
    echo "LC_ALL=ru_RU.UTF-8" >> /etc/default/locale && \
    echo "LANGUAGE=ru_RU.UTF-8" >> /etc/default/locale && \
    ln -s /etc/locale.alias /usr/share/locale/locale.alias && \
    apt-get update && apt-get upgrade -y && apt-get install -y locales

RUN apt-get install -y gosu libpq5 libfreetype6 liblcms2-2 libjpeg62-turbo libwebp6 libtiff5 libmagic1 zlib1g && \
    apt-get install -y libfreetype6-dev liblcms2-dev libjpeg62-turbo-dev libwebp-dev libtiff5-dev && \
    apt-get install -y build-essential libpq-dev zlib1g-dev

COPY api/requirements.txt /
COPY api/requirements-dev.txt /

# Install requirements
RUN pip install -r /requirements.txt -r /requirements-dev.txt

# Create directory for code
RUN mkdir -p /opt/project/api

# Copy source code
COPY api /opt/project/api

COPY api/wait-for-it.sh api/docker-entrypoint.sh /usr/local/bin/

RUN useradd -d /home/${username} -G sudo -u ${uid} ${username} && \
    chmod u+s /usr/sbin/gosu && chmod +x /usr/local/bin/wait-for-it.sh /usr/local/bin/docker-entrypoint.sh

WORKDIR /opt/project/api

# Copy gunicorn config to home directory
COPY configs/gunicorn/gunicorn.${environment}.ini /opt/project/api/gunicorn.ini

USER user
EXPOSE 8080
ENTRYPOINT ["docker-entrypoint.sh"]
