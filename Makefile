help:
	@echo "to check the registry, run 'make lint'"
	@echo "to rebuild MODELS.md from research/data, run 'make tables'"
	@echo "to rebuild the usecase rollup, run 'make usecase'"
	@echo "to re-derive sampler provenance, run 'make samplers'"
	@echo "to re-derive llama.cpp support, run 'make runtime'"
	@echo "to run the steps that ask a model, run 'make llm'"
	@echo "to decide what they proposed, run 'make llm-review' ('make llm-report' just lists)"
	@echo "to refresh published quant sweeps, run 'make curves'"
	@echo "to rebuild the github pages viewer, run 'make site'"
	@echo "to test the viewer end to end, run 'make test-e2e'"
	@echo "to run the whole research sweep, run 'make sweep'"
	@echo "to see what a sweep left for a human, run 'make sweep-report'"
	@echo "to check everything before committing, run 'make precommit'"
.PHONY: help

lint:
	./scripts/models-validate
	./scripts/resolve-turns --check
	./scripts/resolve-samplers --check
	./scripts/resolve-runtime --check
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

# which llama.cpp release loads each model, from llama.cpp's own history
runtime:
	cd research && ./fetch-llama-support
	./scripts/resolve-runtime --write
.PHONY: runtime

# the steps that ask a model rather than a source. both skip themselves unless
# AIMBOT_LLM_URL/MODEL/KEY are set, so this is a no-op on a machine with nothing
# listening. neither writes a fact: see research/llm.py and CONTRIBUTING.md.
llm:
	cd research && ./propose --check
	cd research && ./propose
	cd research && ./score-sentiment
.PHONY: llm

# decide the proposals: shows the evidence for each and records the answer, so
# a row you have looked at never comes back
llm-review:
	cd research && ./propose --review
.PHONY: llm-review

# what the llm steps proposed last time, without asking anything
llm-report:
	cd research && ./propose --report
	cd research && ./score-sentiment --report
.PHONY: llm-report

# the per-model rollup every measurement lands in. sentiment first, because
# usecase joins it.
usecase:
	cd research && ./analyze-task-mentions --json data/sentiment.json
	cd research && ./analyze-usecase
.PHONY: usecase

site:
	./scripts/build-viewer
.PHONY: site

# the page shipped, booted under node against the real data.json. it needs the
# built docs/, so build them first rather than testing a stale copy.
test-e2e: site
	./tests/e2e
	./tests/collectors
.PHONY: test-e2e

test: test-e2e
.PHONY: test

# the whole research sweep: collect, derive, build, check, then the punch list
sweep:
	./scripts/sweep
.PHONY: sweep

# what the last sweep found that only a human can decide
sweep-report:
	./scripts/sweep --report
.PHONY: sweep-report

precommit: lint test-e2e
.PHONY: precommit
