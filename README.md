# Django RESTful SPA based on Vue.js and uses JWT

The project demonstrates the classic TODO list single-page application.

Front-end side based on the progressive JavaScript framework named Vue.js.

The authentication method implements JSON Web-Token (JWT) by default.
Project has custom User model which combined with basic authentication.

Please visit the production version here <a href="https://oleksii-velychko-django-vue.herokuapp.com">
https://oleksii-velychko-django-vue.herokuapp.com</a> which was deployed on Heroku.

> test username: django@django.dev

> test password: 0123456789

![alt text](https://raw.githubusercontent.com/oleksii-velychko/django-vue/master/screenshot.png)

In order to run project to follow next steps:

1. Clone project and install virtual environment into root directory:

    ```
    virtualenv -p python venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Then execute Django commands:

    ```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser (optional)
    ```

3. From ~project/spa/static/spa build client's SPA:

   ```
   npm install
   npm run build
   ```

Run application by `python manage.py runserver 127.0.0.1:9000`
