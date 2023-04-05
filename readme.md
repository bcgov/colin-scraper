# Overview
Web scraper to scrape COLIN-UI and download all the filing outputs of legacy businesses and transfer them into LEAR  
[RFC]()
[design for LEAR side](https://app.zenhub.com/workspaces/relationships-team-space-61435c47e483c4000f08e9f6/issues/gh/bcgov/entity/15341)

# Prerequisites
- fill [.env](https://github.com/MatthewCai2002/env_templates/blob/master/.env) in root directory, [configMap.yaml](https://github.com/MatthewCai2002/env_templates/blob/master/configMap.yaml) under scripts/deployments, and [tnsnames.ora](https://github.com/MatthewCai2002/env_templates/blob/master/tnsnames.ora) under config  
- create `test-outputs` folder in the root directory if not already present  
- linux environment to clone and run app, ie: WSL2 with ubuntu 20.04 installed   
- Gov VPN installed and running to connect to oracle DB     
- **minikube** for local kubernetes deployment
- **docker desktop** installed and enabled in WSL2, to manage containers  
- run `make setup` to setup venv with dev requirements  

# common errors
ORA-12545: Connect failed because target host or object does not exist: usually because VPN is not running when running app or deployment   
sometimes selenium-grid may throw a bind(): failed error, usually resolved by restarting computer

# Running the app
1. set command_executor in scraper.py to "http://selenium:4444/wd/hub"
2. run `make dev` in root directory after which, this only needs to be run if the dockerfile is changed,  
for normal development you can run `docker compose up` 
3. colin-scraper-app will usually crash on startup since it doesn't wait for a chrome node to be setup by selenium grid.   
a workaround is to go into docker desktop and restart the container
4. you should now see 2 dates followed by business numbers being logged
5. if you want to input your own dates, you can update DATE_RANGE_START, DATE_RANGE_END, and FINAL_END_DATE env vars then   
run `docker compose up` 

# Kubernetes Deployment
1. start kubernetes cluster ie: `minikube start`
2. run `eval $(minikube -p minikube docker-env)`
3. set command_executor to "http://selenium-hub:4444/wd/hub"
4. run `make local-deploy`, this sets up local selenium-hub and scraper deployments  
warnings about the oracl-instantclient are normal and expected here
5. use kubectl commands to explore deployment

# Implementation Details
This application connects to COLIN's Oracle DB to query the events table for corp nums and filing events between a specified time interval.  
It then navigates through COLIN UI and searches each queried corp num using selenium.  
For each corp searched it:  
1. harvests all hrefs for outputs attached to filings done within the specified time interval using BS  
2. makes asynchronous download requests for all harvested hrefs.  
3. these request return PDF data which is stored in memory  
4. this data is **temporarily** written into PDF files,  
    a. filing event id, date filled, and name are all available alongside the PDF data  
    b. in the end we want this data to be sent to LEAR's Doc Store  

After all corps with filing events have been visited the time interval is stepped up by a year  
This approach to gathering outputs ensures that we aren't redownloading any outputs and we aren't revisiting corps unnecessarily.  
It also catches any new filing events made during or after the bot runs because we're querying through filing events which means that when a new filing is made we can just start up the bot and tell it to run from when it last ran to the present day and it will grab all the filing events in that time interval and download all the associated outputs.  
Furthermore, scannings of old paper filngs into digital filings are also caught since they create filing events with a timestamp on the day they were scanned. So the bot can just be ran again to catch those.
