#!make
VERSION := $(shell cat src/http_stream_xml/version.py | cut -d= -f2 | sed 's/\"//g; s/ //')
export VERSION

.HELP: version ## Show the current version
version:
	echo ${VERSION}

.HELP: ver-bug ## Bump the version for a bug
ver-bug:
	bash ./scripts/verup.sh bug

.HELP: ver-feature ## Bump the version for a feature
ver-feature:
	bash ./scripts/verup.sh feature

.HELP: ver-release ## Bump the version for a release
ver-release:
	bash ./scripts/verup.sh release

.HELP: reqs  ## Upgrade requirements including pre-commit
reqs:
	pre-commit autoupdate
	bash ./scripts/compile_requirements.sh
	pip install -r requirements.txt
	pip install -r requirements.dev.txt

.HELP: docs  ## Build the documentation
docs:
	bash sphinx-build docs docs_build

.HELP: docs-check  ## Check the documentation
docs-check:
	bash sphinx-build docs -W -b linkcheck -d docs_build/doctrees docs_build/html

.HELP: test  ## Run the test suite
test:
	bash ./scripts/test.sh -m "not slow"

.HELP: test-full  ## Run the full test suite
test-full:
	bash ./scripts/test.sh

.HELP: help  ## Display this message
help:
	@grep -E \
		'^.HELP: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".HELP: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'
