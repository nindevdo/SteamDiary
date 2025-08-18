
.PHONY: up

build:
	@echo "Building..."
	docker-compose build

restart:
	@echo "Restarting..."
	docker-compose restart

up:
	@echo "Starting up the app"
	docker-compose up -d

logs:
	@echo "Starting up the app"
	docker-compose logs -f

watch:
	@echo "Watching for changes recursively..."
	@while inotifywait -r -e modify,create,delete,move .; do \
		make build && make restart; \
	done

