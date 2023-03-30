MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################

setup: clean install install-dev ## Setup the project

clean: clean-build clean-pyc ## Clean the project
	rm -rf venv/

clean-build: ## Clean build files
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## Clean cache files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

install: clean ## Install python virtrual environment
	test -f venv/bin/activate || python3 -m venv  $(CURRENT_ABS_DIR)/venv ;\
	. venv/bin/activate ;\
	pip install --upgrade pip ;\
	pip install -Ur requirements.txt

install-dev: ## Install local application
	. venv/bin/activate ; \
	pip install -Ur requirements.txt; \
	pip install -e .

#################################################################################
# COMMANDS -- Docker Image                                                      #
#################################################################################

dev: ## push local image to DockerHub
	docker build -t colin-scraper .
	docker compose up

local-deploy:
	docker build -t colin-scraper .
	bash scripts/start-selenium.sh
	bash scripts/start-scraper.sh