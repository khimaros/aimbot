help:
	@echo "to check the registry, run 'make lint'"
	@echo "to rebuild MODELS.md from research/data, run 'make tables'"
.PHONY: help

lint:
	./scripts/models-validate
	./research/refresh-tables --check
.PHONY: lint

tables:
	./research/refresh-tables
.PHONY: tables

ids:
	./scripts/resolve-ids --write
.PHONY: ids
