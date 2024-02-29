.DEFAULT_GOAL := help 

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: local-setup
local-setup: ## Set up the local environment (e.g. install git hooks)
	scripts/local-setup.sh

.PHONY: test
test: ## Run tests
	docker compose -f lift-pass/docker-compose.yml run -T --rm lift pytest test -ra

.PHONY: check-format
check-format: ## Check format
	docker compose -f lift-pass/docker-compose.yml run --rm --no-deps lift black --check src test

.PHONY: check-typing
check-typing: ## Check typing
	docker compose -f lift-pass/docker-compose.yml run --rm --no-deps lift mypy src test

.PHONY: pre-commit
pre-commit: check-format check-typing test ## Run pre-commit checks
