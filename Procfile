release: python ./manage.py makemigrations && python ./manage.py migrate
web: python ./manage.py collectstatic --no-input; gunicorn project.wsgi --log-file -

