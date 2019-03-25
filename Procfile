release: ./project/spa/static/spa/node_modules/.bin/webpack --config ./project/spa/static/spa/build/webpack.prod.conf.js && python ./manage.py makemigrations && python ./manage.py migrate && python ./manage.py collectstatic --no-input
web: gunicorn project.wsgi --log-file -

