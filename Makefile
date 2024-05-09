.PHONY: convert host publish

convert: scripts/build_htdocs.py
	python scripts/build_htdocs.py

publish: convert
	@echo "Publishing to Readme"
	@rdme docs markdown --version=1.0

host: convert
	@echo "Starting server on http://localhost:8080"
	@python -m http.server 8082 --directory htdocs
