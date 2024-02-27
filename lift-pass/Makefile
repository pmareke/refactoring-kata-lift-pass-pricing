.DEFAULT_GOAL := help 

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: test
test: ## Run tests
	PYTHONPATH=. poetry run pytest test -ra

.PHONY: test-coverage
test-coverage: ## Run tests coverage
	PYTHONPATH=. poetry run coverage run --branch -m pytest test
	poetry run coverage html

.PHONY: format
format: ## Run format
	poetry run black src test

.PHONY: check-format
check-format: ## Check format
	poetry run black --check src test

.PHONY: check-typing
check-typing: ## Check typing
	poetry run mypy src test
