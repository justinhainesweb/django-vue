# Django RESTful SPA based on Vue.js and uses JWT

The project demonstrates the classic TODO list single-page application (SPA).

Front-end side based on the progressive JavaScript framework named Vue.js.

The authentication method implements JSON Web-Token (JWT) by default.
Project has custom User model which combined with basic authentication.

Please visit the production version here <a href="https://alex-djangovue.herokuapp.com">
https://alex-djangovue.herokuapp.com</a> which was deployed on Heroku.

> test username: django@django.dev

> test password: 0123456789

![alt text](https://raw.githubusercontent.com/oleksii-velychko/django-vue/master/screenshot.png)

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
   ```

Output >>
> Cleaning database...<br>
> Got number_of_users: 5<br>
> Got max_projects_per_user: 5<br>
> Got max_tasks_per_user: 5<br>
> Got max_likes_per_user: 5<br>
> Wait...<br>
> Done. Created 5 users, 25 projects, 125 tasks.<br>


Run application by `python manage.py runserver 127.0.0.1:9000`

Also, for using the email verifier add EMAIL_VERIFIER_API_KEY variable to local environment.