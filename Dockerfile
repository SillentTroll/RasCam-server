FROM ubuntu:14.04

MAINTAINER Alexandru Guzun <alex@aguzun.com>

# Update stuff
RUN apt-get update

# Install nginx uwsgi and supervisor
RUN apt-get -y install nginx sed python-pip python-dev uwsgi-plugin-python supervisor
# Install Python Setuptools
RUN apt-get --no-install-recommends install -y python-setuptools build-essential python-dev libpq-dev ca-certificates

# Install pip
RUN easy_install pip

ADD requirements.txt /tmp/requirements.txt

COPY wsgi /var/www/app/wsgi
COPY config /var/www/app/config

# Install requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install supervisor-stdout

RUN mkdir -p /var/log/app

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default

COPY config/flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf

RUN mkdir -p /var/log/supervisor
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

VOLUME ["/var/log/app"]

RUN service nginx stop

CMD supervisord -c /etc/supervisor/conf.d/supervisord.conf -n
