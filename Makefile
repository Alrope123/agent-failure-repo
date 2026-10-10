.DEFAULT_GOAL := help
REPO_OPS ?= /Users/dylanz/working/claude-config/skills/repo-ops/repo_ops.py

.PHONY: help check test hygiene

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	  awk 'BEGIN {FS=":.*?## "} {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

check: hygiene test  ## Run repo hygiene + tests

hygiene:  ## Audit docs + maintainability (repo-ops if available, else inline)
	@if [ -f "$(REPO_OPS)" ]; then \
	  python3 "$(REPO_OPS)" check . ; \
	 else \
	  echo "repo-ops not found; minimal inline check:" ; \
	  for f in README.md PROJECT.md .gitignore docs/ARCHITECTURE.md docs/DECISIONS.md CHANGELOG.md ; do \
	    [ -e "$$f" ] && echo "  ok   $$f" || { echo "  MISS $$f" ; exit 1 ; } ; \
	  done ; \
	 fi

test:  ## Run tests
	@echo 'no tests configured'
