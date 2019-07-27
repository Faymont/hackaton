#!/usr/bin/env bash

set -e

echo "Starting up API server of $PROJECT_NAME project in $ENVIRONMENT environment"

echo "Waiting for Postgres"
wait-for-it.sh \
	--host=${POSTGRES_HOST} \
	--port=${POSTGRES_PORT} \
	--timeout=30 \
	--strict \
	-- echo "Postgres is up"

case "$ENVIRONMENT" in
	"development" | "production")
	    ;;
	*)
		echo "Variable ENVIRONMENT has unsupported value: $ENVIRONMENT"
		exit 1
		;;
esac

echo "Variable DJANGO_SETTINGS_MODULE is set to $DJANGO_SETTINGS_MODULE value"

[ ! -d media ] && mkdir media
[ ! -d static ] && mkdir static
[ ! -d log ] && mkdir log
gosu root chown -R user media static log

echo "Applying migrations"
python manage.py migrate

echo "Collecting static files"
python manage.py collectstatic --no-input --clear

echo "Starting $@"
exec $@
