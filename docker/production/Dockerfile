FROM python:latest

ENV PYTHONUNBUFFERED=1 DOCKER=1 DEBIAN_FRONTEND=noninteractive

## Install dependencies
RUN apt-get update \
    && apt-get --no-install-recommends install -y vim-tiny \
    && apt-get install -my wget gnupg \
    # Install latest NodeJS + NPM
    && apt-get --no-install-recommends install -y curl ca-certificates apt-transport-https lsb-release \
    && curl -sSL https://deb.nodesource.com/setup_7.x | bash - \
    && apt-get --no-install-recommends install -y nodejs \
    # Install global NPM packages
    && npm install -g webpack \
    # System stuff
    && apt-get --no-install-recommends install -y nginx-extras \
    # Cron
    #&& apt-get install -y cron curl zip unzip g++ \
    # Cleanup after installation
    && npm cache clear \
    && rm -rf /tmp/npm-* \
    && apt-get clean -y \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -fr /var/lib/apt/lists/* \
    # Create basic project structure
    && mkdir -p /app/project/assets/ /app/logs /app/tmp/ /sock/

## Setup timezone
RUN echo "Europe/Moscow" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app/

# Add packages.json (NPM) & requirements.txt (PIP) files to the image
ADD project/requirements.txt /app/requirements.txt
ADD project/assets/package.json /app/project/assets/package.json

# Install NPM & Python dependencies & uwsgi
RUN pip install --no-cache-dir --upgrade pip setuptools \
    && pip install -U -r /app/requirements.txt --no-cache-dir \
    # uwsgi compile fails randomly, see https://github.com/unbit/uwsgi/issues/1318` && \
    && (while true; do pip install --no-cache-dir --disable-pip-version-check --verbose uwsgi && break; done)

RUN cd /app/project/assets/ \
    && npm install \
    && npm cache clear

ADD . /app/
ADD docker/production/settings/* /app/project/settings/

RUN cd /app/project/assets/ \
    && npm run build

RUN python manage.py collectstatic --noinput -v0

ADD docker/production/nginx/nginx.conf /etc/nginx/sites-enabled/project
ADD docker/production/nginx/conf.d/* /etc/nginx/conf.d/

EXPOSE 80

EXPOSE 443