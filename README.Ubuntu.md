Install
======

* Install Python 2.6 or hingher version

* Install Django 1.6 version

Download from xxxx.

* Install Celery 3.1
* Install rabbitmq-server
* Install Apache

Install RabbitMQ-Server:

* Install erlang:

> zypper addrepo http://download.opensuse.org/repositories/server:/database/SLE_11_SP1 database
> zypper addrepo http://download.opensuse.org/repositories/devel:/languages:/erlang/SLE_11_SP1 erlang
> zypper install erlang

* Install RabbitMQ-Server

> zypper addrepo http://download.opensuse.org/repositories/devel:/languages:/python/SLE_11_SP1 python
> zypper install rabbitmq-server

Install Apache

> zypper install apache2

How to use run it 
======

* python manage.py runserver
* celery -A ecloud worker --concurrency=4 -l debug -B -S djcelery.schedulers.DatabaseScheduler

* Fill database:
StatusType: active, running, expired, shutdown
Template: Template
Resource: 4CPU/8G RAM/50G Disk/9 Flavor

Init Database
======

* login /admin
* fill image, statustype tables

https://github.com/asaglimbeni/django-datetime-widget/archive/master.zip
