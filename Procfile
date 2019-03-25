release: python ./manage.py makemigrations && python ./manage.py migrate
compile: python ./manage.py collectstatic --no-input
web: gunicorn project.wsgi --log-file -

