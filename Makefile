SHELL := /usr/bin/bash

# description: 
.PHONY: venv
venv:
	@if [ -d "venv" ]; then \
		echo 'virtualenv already exists'; \
		echo 'please `rm -rf venv` and run again.'; \
	 else \
	 	virtualenv venv && \
		source venv/bin/activate && \
		pip install -r requirements.txt; \
	 fi
.PHONY: test
test:
	@pytest -v

.PHONY: validate-config
validate-config:
	@pytest -vk TestFallbackConfig

.PHONY: docs
docs:
	doxygen -q docs/Doxyfile
