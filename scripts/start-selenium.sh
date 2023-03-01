# Connect to cluster
kubectl cluster-info --context kind-kind
# Start Selenium Hub
kubectl create --filename=/colin-scraper/deployment/selenium-hub-deployment.yaml
# Start Service
kubectl create --filename=/colin-scraper/deployment/selenium-hub-svc.yaml
# Start Selenium Nodes
sleep 40s
kubectl create --filename=selenium-node-chrome-deployment.yaml