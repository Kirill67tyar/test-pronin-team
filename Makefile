COMPOSE_FILE = docker-compose.yml

up:
	docker compose -f $(COMPOSE_FILE) up -d --build

down:
	docker compose -f $(COMPOSE_FILE) down -v

reload:
	docker compose -f $(COMPOSE_FILE) down -v && docker compose -f $(COMPOSE_FILE) up -d --build
	
run-migrate:
	chmod +x ./run_migrate.sh
	./run_migrate.sh
