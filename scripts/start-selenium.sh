# Connect to cluster
kubectl cluster-info --context kind-kind
# Start Selenium Hub
kubectl create --filename=./deployment/selenium-hub-deployment.yaml
# Start Service
kubectl create --filename=./deployment/selenium-hub-service.yaml
# Start Selenium Nodes
sleep 40s
kubectl create --filename=./deployment/selenium-node-chrome.yaml