# start config map
kubectl apply -f scripts/deployment/configMap.yaml
# start scraper
kubectl apply -f scripts/deployment/colin-scraper-deployment.yaml

kubectl get po