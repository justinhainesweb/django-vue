#!/usr/bin/env bash

cd "$1" || exit 1
echo "-----> Build Vue.js"
./project/spa/static/spa/node_modules/.bin/webpack --config ./project/spa/static/spa/build/webpack.prod.conf.js
echo "-----> Collecting static files"
python manage.py collectstatic --noinput --traceback