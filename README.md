# Django RESTful SPA based on Vue.js and uses JWT

The project demonstrates the classic TODO list single-page application (SPA).

Front-end side based on the progressive JavaScript framework named Vue.js.

The authentication method implements JSON Web-Token (JWT) by default.
Project has custom User model which combined with basic authentication.

> test username: django@django.dev

> test password: 12345678

In order to run project to follow next steps:

1. Clone project and install virtual environment inside root directory:

    ```
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Then execute Django commands:

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

3. Build client SPA:

   ```
   npm install --prefix ./project/spa/static/spa
   npm run build --prefix ./project/spa/static/spa
   python manage.py collectstatic --noinput --link
   ```
   
4. Fill database a seed data (edit load_data.cfg for setting up custom values):

   ```
   python manage.py load_data

Run application by `python manage.py runserver 127.0.0.1:9000`
