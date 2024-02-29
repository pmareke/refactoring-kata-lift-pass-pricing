.DEFAULT_GOAL := help 

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: test
test: ## Run tests
	docker compose run -T --rm lift pytest test -ra

.PHONY: test-coverage
test-coverage: ## Run tests coverage
	docker compose run --rm lift coverage run --branch -m pytest test
	docker compose run --rm lift coverage html
	@echo "You can open the coverage report here: ${PWD}/htmlcov/index.html"

.PHONY: format
format: ## Run format
	docker compose run --rm --no-deps lift black src test

.PHONY: check-format
check-format: ## Check format
	docker compose run --rm --no-deps lift black --check src test

.PHONY: check-typing
check-typing: ## Check typing
	docker compose run --rm --no-deps lift mypy src test
