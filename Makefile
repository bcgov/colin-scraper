MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################

setup: clean install install-dev ## Setup the project

clean: clean-build clean-pyc ## Clean the project
	sudo rm -rf venv/

clean-build: ## Clean build files
	sudo rm -fr build/
	sudo rm -fr dist/
	sudo rm -fr .eggs/
	find . -name '*.egg-info' -exec sudo rm -fr {} +
	find . -name '*.egg' -exec sudo rm -fr {} +

clean-pyc: ## Clean cache files
	find . -name '*.pyc' -exec sudo rm -f {} +
	find . -name '*.pyo' -exec sudo rm -f {} +
	find . -name '*~' -exec sudo rm -f {} +
	find . -name '__pycache__' -exec sudo rm -fr {} +

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

dev: ## build image and compose network
	docker build -t colin-scraper .
	docker compose up

local-deploy: ## build local image and make deployment
	docker build -t colin-scraper .
	bash scripts/start-selenium.sh
	bash scripts/start-scraper.sh