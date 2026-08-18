help:
	@echo "to check the registry, run 'make lint'"
	@echo "to rebuild MODELS.md from research/data, run 'make tables'"
	@echo "to rebuild the usecase rollup, run 'make usecase'"
	@echo "to re-derive sampler provenance, run 'make samplers'"
	@echo "to refresh published quant sweeps, run 'make curves'"
	@echo "to rebuild the github pages viewer, run 'make site'"
.PHONY: help

lint:
	./scripts/models-validate
	./scripts/resolve-turns --check
	./scripts/resolve-samplers --check
	cd research && ./fetch-quant-sweeps --check
	./research/refresh-tables --check
	cd research && ./analyze-usecase --check
	./scripts/build-viewer --check
.PHONY: lint

tables:
	./research/refresh-tables
.PHONY: tables

ids:
	./scripts/resolve-ids --write
.PHONY: ids

# published per-quant quality sweeps, where a quantizer measured their own work
curves:
	cd research && ./fetch-quant-sweeps
.PHONY: curves

# what each sampling profile's numbers still agree with
samplers:
	./scripts/resolve-samplers --write
.PHONY: samplers

turns:
	cd research && ./analyze-chat-templates --json data/template-probes.json
	./scripts/resolve-turns --write
.PHONY: turns

# the per-model rollup every measurement lands in. sentiment first, because
# usecase joins it.
usecase:
	cd research && ./analyze-task-mentions --json data/sentiment.json
	cd research && ./analyze-usecase
.PHONY: usecase

site:
	./scripts/build-viewer
.PHONY: site
