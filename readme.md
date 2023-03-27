# Overview
Web scraper to scrape COLIN-UI and download all the filing outputs of legacy businesses and transfer them into LEAR  

# Prerequisites
fill [.env](https://github.com/MatthewCai2002/env_templates/blob/master/.env) in root directory, [configMap.yaml](https://github.com/MatthewCai2002/env_templates/blob/master/configMap.yaml) under scripts/deployments, and [tnsnames.ora](https://github.com/MatthewCai2002/env_templates/blob/master/tnsnames.ora) under config  
create `test-outputs` folder in the root directory if not already present
Python 10+   
linux environment to clone and run app   
Gov VPN installed and running to connect to oracle DB   
minikube for local kubernetes deployment

# common errors
VPN not running when running app or deployment   
sometimes selenium-grid may throw a bind(): failed error, usually resolved by restarting computer


# Running the app
1. create config folder with a tnsnames.ora file with connection credentials to connect to COLIN Oracle DB
2. set command_executor in scraper.py to "http://selenium:4444/wd/hub"
3. run `make image` in root directory
4. run `docker compose up` in root directory
5. colin-scraper-app will usually fail since it doesn't wait for a chrome node to be setup by selenium grid.   
a workaround is to go into docker desktop and restart the container
6. you should now see 2 dates followed by business numbers being printed
7. if you want to input your own dates, you can update DATE_RANGE_START, DATE_RANGE_END, and FINAL_END_DATE env vars then   
run `make image` again

# Kubernetes Deployment
1. start kubernetes cluster
2. set command_executor to "http://selenium-hub:4444/wd/hub"
3. build the image and push to matthewcai/colin-scraper
4. cd into scripts and run bash start-selenium.sh
5. run bash start-scraper.sh

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
