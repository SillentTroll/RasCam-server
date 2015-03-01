# RasCam-server
Server part of [RasCam](https://github.com/SillentTroll/rascam) project.

Does the management of the configured cameras and captured images.

##Whats inside?
 - [flask](http://flask.pocoo.org), [nginx](http://nginx.org) and [uwsgi](http://uwsgi-docs.readthedocs.org/en/latest/) doing the web server stuff
 - [AngularJS](https://angularjs.org) for web client side
 - [MongoDB](https://www.mongodb.com) as the database
 - [Redis](http://redis.io) for caching

##Installation
I have decided to use [Docker](https://www.docker.com) and [docker-compose](https://github.com/docker/compose) for app management and deploy.
So, assuming your already have a server accessible from your Raspberry Pi device, ssh into it and execute:
```
git clone https://github.com/SillentTroll/rascam_server
cd rascam_server
fig build
fig up -d
```
It will get latest version, build the Docker containers and run them all in background. Pretty neat, right?

##Configuration
Open a browser and go to your server. 
First of all you will have to register the admin user:
![](https://raw.githubusercontent.com/SillentTroll/rascam_server/master/images/first_config.png)
Now login with the newly created user and feel the power!
![](https://raw.githubusercontent.com/SillentTroll/rascam_server/master/images/login.png)
You can now go and configure the Raspberry Pi.