web: gunicorn project.wsgi --log-file -
release: python3 ./manage.py migrate && release: python3 ./manage.py collectstatic --no-input
