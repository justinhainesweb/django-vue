# Django RESTful SPA based on Vue.js and uses JWT

The project demonstrates classic TODO list single-page application.

The front-end side based on amazing reactive library Vue.js.

The authentication method implements the JSON Web-Token (JWT) by default.
Project has custom User model which combined with basic authentication.

Please visit the production version here <a href="https://oleksii-velychko-django-vue.herokuapp.com">https://oleksii-velychko-django-vue.herokuapp.com</a>

> test username: django@django.dev

> test password: 0123456789

![alt text](https://raw.githubusercontent.com/oleksii-velychko/django-vue/master/screenshot.png)

In order to run project to follow next steps:

1. Clone project and install virtual environment:

    ```
    virtualenv -p python venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Execute Django commands:

    ```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser (optional)
    ```

3. Then need to build client's SPA:

 - Go to ~project/apps/spa/static/spa and execute `npm install`
 - Also from ~project/apps/spa/static/spa and execute execute `npm run build`
 - Then copy files to static directory `python manage.py collectstatic`
 - Run application `python manage.py runserver 127.0.0.1:9000`
