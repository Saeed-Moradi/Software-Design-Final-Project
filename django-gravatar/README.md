# Django Gravatar

[![PyPI version](https://badge.fury.io/py/django-simple-gravatar.png)](http://badge.fury.io/py/django-simple-gravatar)
[![Downloads](https://pypip.in/d/django-simple-gravatar/badge.png)](https://crate.io/packages/django-simple-gravatar)
[![Build](https://travis-ci.org/skitoo/django-gravatar.png)](https://travis-ci.org/skitoo/django-gravatar)
[![Coverage Status](https://coveralls.io/repos/skitoo/django-gravatar/badge.png)](https://coveralls.io/r/skitoo/django-gravatar)

Django Gravatar is a lightweight Django application that allows you to insert a Gravatar image in your templates.


## Get it

The best way to install Django Gravatar is use pip.

```
pip install django-simple-gravatar
```

If you prefer install it from source, grab the git repository from github and run setup.py

```
$ git clone git://github.com/skitoo/django-gravatar.git
$ cd django-gravatar
$ python setup.py install
```

# Installation

Now Django Gravatar is in your **PYTHONPATH**. You can add this app in your project settings.py file.

```python
INSTALLED_APPS = (
   # other apps
   'django_gravatar',
)
```

You can specify a default image url, Gravatar will use it if it cannot find an account associated with the email parameter.
In your settings project file add this variable

```python
GRAVATAR_DEFAULT_URL = "http://www.example.com/mydefaultavatar.jpg"
```

You can also tell Gravatar to use https instead of http by adding this variable

```python
GRAVATAR_SECURE = True
```

# Usage

Now you can use Django Gravatar tag in your templates.
First import template tag.

```
{% load gravatar %}
```

Django Gravatar offers you two tags. The first one return gravatar image url.

```
{% gravatar_url user.email %}

# you can pass an optional argument to specify the avatar size. By default size is 80.

{% gravatar_url user.email 40 %}
```

The second one return an HTML img tag.

```
{% gravatar user.email %}

# you can also pass an optional size argument here.

{% gravatar user.email 40 %}

# this tag provides another argument to specify <img /> arguments.

{% gravatar user.email 40 'class="gravatar"' %}
```

## Credits

Alexis Couronne <alexis.couronne@gmail.com>


