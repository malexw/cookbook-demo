.PHONY: convert host

convert: scripts/build_htdocs.py
	python scripts/build_htdocs.py

host: convert
	@echo "Starting server on http://localhost:8080"
	@python -m http.server 8082 --directory htdocs
