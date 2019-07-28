test_pattern = *
environment = development
current_time = $(shell date +'%Y%m%d_%H%M%S')

prepare_envs:
	[ -f ./api/.env ] || cp configs/environment/$(environment).env api/.env
	ln -sf api/.env .env

install:
	@make -s check
	cd api && make install
	# Ставим линтеры.
	@if [ "$(environment)" = "development" ] ; then \
		npm i;\
	fi
	@make prepare_envs

build:
	@make -s check
	@make prepare_envs
	docker-compose build --pull

up:
	@make -s check
	@make prepare_envs
	docker-compose up --build -d

api_shell:
	docker-compose exec api bash

db_shell:
	docker-compose exec postgres psql hackaton -U for_people

fixtures:
	@if [ "$(environment)" = "development" ] ; then\
		docker-compose exec api ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser(email='samskripka@gmail.com', username='admin', password='adminadmin') if (User.objects.filter(username='admin').count() == 0) else None";\
	fi
	#docker-compose exec api sh -c "./manage.py loaddata apps/tests/fixtures/*.json"

check:
	@if [ "$(environment)" = "development" ] && [ ! -f configs/environment/development.env ] ; then\
		echo "File development.env doesn't exist";\
		exit 1;\
	fi

	@if [ "$(environment)" = "production" ] && [ ! -f configs/environment/production.env ] ; then\
		echo "File production.env doesn't exist";\
		exit 1;\
	fi

linter:
	cd api && make linter