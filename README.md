# Django Chef's Recipe Project

This application allows a chef to publish his own secret recipes and also enables the chef to conduct workshops based on his recipes. General customers can book a workshop published by the chef.

## 1. Requirements :

* Python 3.x (you can install [python](https://www.python.org/downloads/))
* Django  (you can install [Django](https://docs.djangoproject.com/en/3.2/topics/install/))
* **pip** package management system -
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
