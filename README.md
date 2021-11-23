# kopf-operator
HelloWorld kopf Python Operator for Kubernetes

### Requirements

1. `kind` and `kubectl` are installed.
2. Python >=3.7 is installed

### Setup

1. Create the kind cluster.
```bash
kind create cluster --config cluster.yaml
```

2. Create the kubectl config file.
```bash
kubectl cluster-info --context kind-hub
```

3. Create the `DemoWeb` CustomResourceDefinition.
```bash
kubectl apply -f crd-resources/crd.yaml
```

4. Install kopf and kubernetes Python packages.
```bash
pip3 install -r requirements.txt
```

5. Run the operator.
```bash
kopf run operator.py
```

6. Create the resources.
```bash
kubectl apply -f sealneaward-demoweb.yaml
```

### Access Deployment

1. Get the service.
```bash
kubectl get svc
```

2. Port forward to the service.
```
kubectl port-forward svc/sealneaward-svc 8080:8080
```

### Delete Deployment

1. Delete the resources.
```bash
kubectl delete -f sealneaward-demoweb.yaml
```
