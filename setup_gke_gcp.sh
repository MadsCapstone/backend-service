# Install ingress-nginx to cluster
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.48.1/deploy/static/provider/cloud/deploy.yaml

#setup flask app
kubectl apply -f kubefiles/flask_app-deploy.yaml
kubectl apply -f kubefiles/flask_app-service.yaml

#setup react app
kubectl apply -f kubefiles/react-app-deploy.yaml
kubectl apply -f kubefiles/react-app-service.yaml

# setup ingress controller behind a load balancer
kubectl apply -f kubefiles/fanout-ingress-initial.yaml

# Install cert manager
kubectl apply -f https://github.com/jetstack/cert-manager/releases/latest/download/cert-manager.yaml

# setup clusterissuer
kubectl apply -f kubefiles/acme_issuer_private_key.yaml

# setup ingress controller behind a load balancer
kubectl apply -f kubefiles/fanout-ingress-final.yaml


###SQL PROXY CONNECTION###
#add service account
kubectl create secret generic gen-capstone-svc-acct --from-file=service_account.json=ermias-biz-3ea221b65810.json


