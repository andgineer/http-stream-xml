#!make
VERSION := $(shell cat src/http_stream_xml/version.py | cut -d= -f2 | sed 's/\"//g; s/ //')
export VERSION

version:
	echo ${VERSION}

ver-bug:
	bash ./scripts/verup.sh bug

ver-feature:
	bash ./scripts/verup.sh feature

ver-release:
	bash ./scripts/verup.sh release

reqs:
	pre-commit autoupdate
	bash ./scripts/compile_requirements.sh
	pip install -r requirements.txt
	pip install -r requirements.dev.txt

docs:
	bash ./scripts/docs.sh

docs-check:
	bash sphinx-build docs -W -b linkcheck -d docs_build/doctrees docs_build/html
