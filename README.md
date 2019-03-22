# Django RESTful SPA based on Vue.js and uses JWT

The project demonstrates classic TODO list single-page application.

The front-end side based on amazing reactive library Vue.js.

The authentication method implements the JSON Web-Token (JWT) by default.
Project has custom User model which combined with basic authentication.

Please visit the production version on <a href="https://django-vue.herokuapp.com/">https://django-spa-todo.herokuapp.com/</a>

> test username: django@django.dev

> test password: djangodjango

![alt text](https://raw.githubusercontent.com/oleksii-velychko/django-vue/master/screenshot.png)

In order to run the project to follow next steps:

1. Clone the project and install virtual environment:

    ```
    virtualenv -p python3 venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```

2. Execute Django commands:

    ```
    python3 ./manage.py makemigrations
    python3 ./manage.py migrate
    python3 ./manage.py createsuperuser
    ```

3. Then needs to build client's SPA:

 - Go to ~project/apps/spa/static/spa and execute `npm install`
 - Then create build as command from project root directory
 `project/spa/static/spa/node_modules/.bin/webpack --config project/spa/static/spa/build/webpack.dev.conf.js --progress --colors --watch`
 - Then copy files to static directory `python3 ./manage.py collectstatic`
 - Run application `python3 ./manage.py runserver 127.0.0.1:9000`
