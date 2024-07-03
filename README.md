# Hitotose-Django

## Memo

``` sh
# Install Django
pip install Django

# Install Djongo (MongoDB)
pip install djongo

# Install Django Rest Framework
pip install djangorestframework

# Install PyMongo
pip install pymongo[snappy,gssapi,srv,tls]

# Install dnspython for using mongodb+srv:// URIs with the command
pip install dnspython

# Create a new Django project
django-admin startproject [hitotose]

# Create a new Django app with the project
python manage.py startapp [api]

# Add the app to `settings.py`
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'api',
]

# Define a model

```
