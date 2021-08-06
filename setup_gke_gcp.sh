# Install ingress-nginx to cluster
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.48.1/deploy/static/provider/cloud/deploy.yaml

# Install cert manager
kubectl apply -f https://github.com/jetstack/cert-manager/releases/latest/download/cert-manager.yaml

#setup flask app
kubectl apply -f kubefiles/flask_app-deploy.yaml
kubectl apply -f kubefiles/flask_app-service.yaml

#setup react app
kubectl apply -f kubefiles/react-app-deploy.yaml
kubectl apply -f kubefiles/react-app-service.yaml

# setup ingress controller behind a load balancer
kubectl apply -f kubectl/fanout-ingress.yaml