# Overview
Web scraper to scrape COLIN-UI and download all the filing outputs of legacy businesses and transfer them into LEAR 

# Running the app
1. setup .env and configMap.yaml with environment variables
2. create tnsnames.ora in config with connection credentials to connect to COLIN Oracle DB
3. run make setup to install requirements and setup venv
4. set command_executor in scraper.py to "http://selenium:4444/wd/hub"
5. run docker compose up in root directory

# Deployment
set command_executor to "http://selenium-hub:4444/wd/hub"
cd into scripts and run bash start-selenium.sh
then run bash start-scraper.sh