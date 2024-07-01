# Hitotose-Django

## Memo

``` sh
# Install Django
pip install Django

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