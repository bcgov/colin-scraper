# start config map
kubectl apply -f deployment/configMap.yaml
# start scraper
kubectl apply -f deployment/colin-scraper-deployment.yaml