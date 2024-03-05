.DEFAULT_GOAL := help 

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the chatcommands Docker image
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose -f lift-pass/docker-compose.yml build

.PHONY: local-setup
local-setup: ## Set up the local environment (e.g. install git hooks)
	scripts/local-setup.sh

.PHONY: test
test: ## Run tests
	docker compose -f lift-pass/docker-compose.yml run -T --rm lift pytest test -ra

.PHONY: watch
watch: ## Watch tests
	docker compose -f lift-pass/docker-compose.yml run -T --rm lift ptw

.PHONY: test-coverage
test-coverage: ## Run tests coverage
	docker compose -f lift-pass/docker-compose.yml run --rm lift coverage run --branch -m pytest test
	docker compose run --rm lift coverage html
	@echo "You can open the coverage report here: ${PWD}/htmlcov/index.html"

.PHONY: format
format: ## Run format
	docker compose  -f lift-pass/docker-compose.yml run --rm --no-deps lift black src test

.PHONY: check-format
check-format: ## Check format
	docker compose -f lift-pass/docker-compose.yml run --rm --no-deps lift black --check src test

.PHONY: check-typing
check-typing: ## Check typing
	docker compose -f lift-pass/docker-compose.yml run --rm --no-deps lift mypy src test

.PHONY: pre-commit
pre-commit: check-format check-typing test ## Run  pre-commit checks
