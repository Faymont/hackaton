venv=python3
environment=development
DEV_ARGS=DJANGO_SETTINGS_MODULE=project.settings \
	IS_FULL_PATH_TO_FILE=1 \
	PATH_TO_FILE=../log/django.log

install:
	[ -d $(venv) ] || virtualenv -p python3 $(venv)
	@make pip_install venv=$(venv) environment=$(environment)

pip_install:
	$(venv)/bin/pip install -r requirements.txt
	if [ "$(environment)" = "development" ] ; then \
		$(venv)/bin/pip install -r requirements-dev.txt ; \
	fi

migrate:
	$(DEV_ARGS) $(venv)/bin/python manage.py makemigrations
	$(DEV_ARGS) $(venv)/bin/python manage.py migrate

un-migrate:
	$(DEV_ARGS) $(venv)/bin/python manage.py migrate for_people 0001_initial

start-app:
	$(DEV_ARGS) $(venv)/bin/python manage.py startapp blog ./apps/blog

linter:
	$(venv)/bin/prospector

test:
	$(venv)/bin/py.test apps/ -s

runserver:
	$(DEV_ARGS) $(venv)/bin/python manage.py runserver

shell:
	$(DEV_ARGS) $(venv)/bin/python manage.py shell

shell_plus:
	if [ "$(environment)" = "development" ] ; then \
		$(DEV_ARGS) $(venv)/bin/python manage.py shell_plus --notebook ; \
	fi

dump_fixtures:
	$(DEV_ARGS) $(venv)/bin/python manage.py dumpdata $(APPS_ARGS) --natural-foreign --indent 4

load_fixtures:
	$(DEV_ARGS) $(venv)/bin/python manage.py loaddata apps/tests/fixtures/*.json

make_messages:
	$(DEV_ARGS) $(venv)/bin/python manage.py makemessages -l en -i python3

compile_messages:
	$(DEV_ARGS) $(venv)/bin/python manage.py compilemessages -l en