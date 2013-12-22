## Install ##

The ECloud requires below softwares:

* Python 2.6 or hingher version
* Django 1.6 version
* Celery
* Rabbitmq-server
* Apache web

### Install Django 1.6 ###

<pre><code>
# wget https://www.djangoproject.com/download/1.6.1/tarball/
# tar xzvf Django-1.6.1.tar.gz
# cd Django-1.6.1
# python setup.py install
</code></pre>

### Install Celery ###

 Download from https://pypi.python.org/pypi/celery/
<pre><code>
# wget --no-check-certificate https://pypi.python.org/packages/source/c/celery/celery-3.1.7.tar.gz
# tar zxvf celery-3.1.7.tar.gz
# cd celery-3.1.7
# python setup.py install
</code></pre>

### Install erlang ###
<pre><code>
# zypper addrepo http://download.opensuse.org/repositories/server:/database/SLE_11_SP1 database
# zypper addrepo http://download.opensuse.org/repositories/devel:/languages:/erlang/SLE_11_SP1 erlang
# zypper install erlang
</code></pre>

### Install RabbitMQ-Server ###
<pre><code>
# zypper addrepo http://download.opensuse.org/repositories/devel:/languages:/python/SLE_11_SP1 python
# zypper install rabbitmq-server
</code></pre>

### Install Apache ###
<pre><code>
# zypper install apache2
</code></pre>

## How to use run it ##

Start server under development without apache server mode:
<pre><code>
# python manage.py runserver 127.0.0.0:8000
# python manage.py celery worker --loglevel=info -B -S djcelery.schedulers.DatabaseScheduler
</code></pre>

Fill database:

- StatusType: rebooting, running, expired, shutdown
- Template: Template
- Resource: 4CPU/8G RAM/50G Disk/9 Flavor

