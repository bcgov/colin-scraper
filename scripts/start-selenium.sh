# Connect to cluster
kubectl cluster-info
# Start Selenium Hub
kubectl create --filename=scripts/deployment/selenium-hub-deployment.yaml
# Start Service
kubectl create --filename=scripts/deployment/selenium-hub-service.yaml
# Start Selenium Nodes
sleep 40s
kubectl create --filename=scripts/deployment/selenium-node-chrome.yaml
sleep 45s