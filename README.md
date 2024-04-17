# Django Chef's Recipe Project

This application allows a chef to publish his own secret recipes and also enables the chef to conduct workshops based on his recipes. General customers can book a workshop published by the chef.

## 1. Requirements :

* Python 3.x (you can install [python](https://www.python.org/downloads/))
* Django  (you can install [Django](https://docs.djangoproject.com/en/5.0/intro/install/))
* **pip** package management system
* Using a virtual environment is highly recommended - Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io)
* Dependencies in **requirements.txt** (use `pip install -r requirements.txt` to install them)

## 2. Database :
* PostgreSQL is used for this project
* Database structure implementation : use `manage.py migrate` command

In your Django settings.py

```bash
   'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'YOUR DB NAME',
        'USER': 'YOUR DB USERNAME',
        'PASSWORD': 'YOUR DB PASSWORD',
        'HOST': 'YOUR DB HOST',
        'PORT': '5432',
    }
}
```

## 3. Configure Gmail SMTP server:
* under your settings.py file you need to add the following settings
* To use gmail SMTP, we need to enter a password for the SMTP server. Since Google uses a two-step verification process and additional security measures, you cannot use your Google account password directly. Instead, Google allows you to create app-specific passwords for your account. An app password is a 16-digit passcode that gives a less secure app or device permission to access your Google account.

```bash
EMAIL_BACKEND = ‘django.core.mail.backends.smtp.EmailBackend’
EMAIL_HOST = ‘smtp.gmail.com’
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ‘your_account@gmail.com’
EMAIL_HOST_PASSWORD = ‘your password’
```

## 4. Getting Started

1. Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).
2. you can clone or fork the git repo

```bash
$ virtualenv {your virtual env name}
$ source {your virtual env name}/bin/activate
$ pip install -r requirements.txt
$ cd projectname/
$ python manage.py migrate
$ python manage.py runserver

```
Then go to localhost:8000 or 127.0.0.1:8000, and the app should be launched and usable there.

## 5. Tests

To run the tests, cd into the directory where manage.py is:

```bash
$ ./manage.py test

```
If you want to know the test coverage:


```bash
$ coverage run ./manage.py test

```
To get test report and generate report in html file:


```bash
$ coverage report -m

$ coverage html
```

## 6. Verifying PEP 8 Compliance

First, you need to ensure that flake8 is installed in your development environment. You can install it from here [flake8](https://flake8.pycqa.org/en/latest/)

Once flake8 is installed, you can run it from the command line to check the style of your Python code. Navigate to your project's root directory and run:
```
flake8 path/to/your/code/

```
Replace path/to/your/code/ with the actual path to the Python files you want to check. If you want to check all Python files within your project, you can simply run flake8 without specifying a path. For more information check the flake8 documentation.
