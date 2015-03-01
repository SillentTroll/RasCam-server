FROM google/debian:wheezy

MAINTAINER Alexandru Guzun <alex@aguzun.com>

# Update stuff
RUN apt-get update

# Install Python Setuptools
RUN apt-get --no-install-recommends install -y python-setuptools build-essential python-dev libpq-dev ca-certificates

# Install pip
RUN easy_install pip

COPY requirements.txt /tmp/requirements.txt

# Install requirements.txt
RUN pip install -r /tmp/requirements.txt

EXPOSE 5000

VOLUME ["/opt/webapp"]

ENTRYPOINT ["python", "/opt/webapp/wsgi/server.py"]
CMD ["runserver"]
