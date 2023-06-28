override SHELL := /bin/bash

.PHONY: help
help: ## Show this help message
	@echo 'Usage:'
	@echo '  make [target] ...'
	@echo
	@echo 'Targets:'
	@grep --no-filename -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	 sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "------------------------------------"

.PHONY: build
build: ## Build images
	docker-compose build

.PHONY: up
up: ## Run app
	docker-compose up -d

.PHONY: down
down: ## Remove containers
	docker-compose down --volumes --remove-orphans

.PHONY: clean
clean: ## Remove all (containers and images)
	docker-compose down --volumes --remove-orphans --rmi all

.PHONY: stop
stop: ## Stop app
	docker-compose stop

.PHONY: logs
logs: ## Show logs
	docker-compose logs -f
