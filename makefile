##
## GLOBAL CONFIG
##
include docker/local/.env

DOCKER_DIR := docker/local
DOCKER_COMPOSE := docker compose -f $(DOCKER_DIR)/docker-compose.yaml
HTTP_PORT := $(PYTHON_EXTERNAL_PORT)

.DELETE_ON_ERROR:
.PHONY: help urls build start watch stop logs destroy bash


help:
	@echo ""
	@echo "Available targets:"
	@echo "   make help            Display this help message"
	@echo "   make urls            Display this project urls"
	@echo "   make build           Build the Docker image"
	@echo "   make watch           Start the Docker containers"
	@echo "   make start           Start the Docker containers in the background"
	@echo "   make stop            Stop the Docker containers"
	@echo "   make logs            Display the logs of Docker containers"
	@echo "   make destroy         Stop and remove Docker containers and volumes"
	@echo "   make bash            Access the Docker container shell"
	@echo ""

urls:
	@echo ''
	@echo 'The available URLs are:'
	@echo '   http://localhost:$(HTTP_PORT)'
	@echo '   http://localhost:$(HTTP_PORT)/docs'
	@echo ''

build:
	@$(MAKE) -s destroy
	@$(DOCKER_COMPOSE) build --no-cache
	@$(MAKE) -s start

start:
	@$(DOCKER_COMPOSE) up -d

watch:
	@$(DOCKER_COMPOSE) up

stop:
	@$(DOCKER_COMPOSE) stop

logs:
	$(DOCKER_COMPOSE) logs -f

destroy:
	@$(DOCKER_COMPOSE) down -v -t 20

bash:
	@docker exec -u root -it petcare bash
