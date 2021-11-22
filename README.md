# kopf-operator
HelloWorld kopf Python Operator for Kubernetes

### Requirements

1. `kind` and `kubectl` are installed.
2. Python >=3.7 is installed

### Setup

1. Create the kind cluster.
```bash
kind create cluster --config cluser.yaml
```

2. Create the kubectl config file.
```bash
kubectl cluster-info --context kind-hub
```

3. Create the `DemoWeb` CustomResourceDefinition.
```bash
kubectl apply -f crd.yaml
```

4. Install kopf and kubernetes Python packages.
```bash
pip3 install -r requirements.txt
```
