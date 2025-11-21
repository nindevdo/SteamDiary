ENVIRONMENT ?= dev
PROJECT_NAME ?= steamdiary

.PHONY: up

up:
	@echo "Bringing up the environment: $(ENVIRONMENT)"
	unset PASS_TMP_ENV GOOGLE_SERVICE_ACCOUNT_JSON_B64;
	@mkdir -m 700 -p /tmp/${PROJECT_NAME}-env; \
	PASS_TMP_ENV=/tmp/${PROJECT_NAME}-env/env-$(ENVIRONMENT); \
	pass show ${PROJECT_NAME}-$(ENVIRONMENT) > $$PASS_TMP_ENV; \
	GOOGLE_JSON_B64=$$(pass show ${PROJECT_NAME}-google-creds | base64 -w 0); \
	echo "GOOGLE_SERVICE_ACCOUNT_JSON_B64=$$GOOGLE_JSON_B64" >> $$PASS_TMP_ENV; \
	echo "services:" > docker-compose.env.yml; \
	echo "  steamdiary:" >> docker-compose.env.yml; \
	echo "    env_file:" >> docker-compose.env.yml; \
	echo "      - $$PASS_TMP_ENV" >> docker-compose.env.yml; \
	docker-compose -f docker-compose.yml -f docker-compose.env.yml up -d --build; \
	rm -f $$PASS_TMP_ENV docker-compose.env.yml;

build:
	@echo "Building..."
	docker-compose build

restart:
	@echo "Restarting..."
	docker-compose restart

logs:
	@echo "Starting up the app"
	docker-compose logs -f

watch:
	@echo "Watching for changes recursively..."
	@while inotifywait -r -e modify,create,delete,move .; do \
		make build && make restart; \
	done
