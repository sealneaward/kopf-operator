import kopf
import kubernetes.client
from kubernetes.client.rest import ApiException
import yaml
import pystache

@kopf.on.create('sealneaward.github', 'v1', 'demowebs')
def create_fn(spec, **kwargs):
    name = kwargs["body"]["metadata"]["name"]
    namespace = kwargs["body"]["metadata"]["namespace"]
    print("Name is %s\n" % name)
    # Create the deployment spec
    doc = yaml.safe_load(f"""
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: {name}-deployment
          namespace: {namespace}
          labels:
            app: {name}
        spec:
          replicas: {spec.get('replicas', 1)}
          selector:
            matchLabels:
              app: {name}
          template:
            metadata:
              labels:
                app: {name}
            spec:
              containers:
              - name: nginx
                image: nginx
                ports:
                - containerPort: 80
                volumeMounts:
                - name: workdir
                  mountPath: /usr/share/nginx/html
              initContainers:
              - name: install
                image: alpine/git
                command:
                - git
                - clone
                - {spec.get('gitrepo', 'https://github.com/sealneaward/sealneaward.github.io.git')}
                - /work-dir
                volumeMounts:
                - name: workdir
                  mountPath: /work-dir
              dnsPolicy: Default
              volumes:
              - name: workdir
                emptyDir: {{}}
    """)

    # Make it our child: assign the namespace, name, labels, owner references, etc.
    kopf.adopt(doc)

    # Actually create an object by requesting the Kubernetes API.
    api = kubernetes.client.AppsV1Api()
    try:
      depl = api.create_namespaced_deployment(namespace=doc['metadata']['namespace'], body=doc)
    except ApiException as e:
      print("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)

    # Create the service spec
    doc = yaml.safe_load(f"""
        apiVersion: v1
        kind: Service
        metadata:
          labels:
            app: {name}
          name: {name}-svc
          namespace: {namespace}
        spec:
          ports:
          - port: 8080
            protocol: TCP
            targetPort: 80
          selector:
            app: {name}
          sessionAffinity: None
          type: ClusterIP
    """)

    # Make it our child: assign the namespace, name, labels, owner references, etc.
    kopf.adopt(doc)

    # Actually create an object by requesting the Kubernetes API.
    api = kubernetes.client.CoreV1Api()
    try:
      svc = api.create_namespaced_service(namespace=doc['metadata']['namespace'], body=doc)
      # Update the parent's status.
      return {'children': [svc.metadata.uid]}
    except ApiException as e:
      print("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)

@kopf.on.delete('sealneaward.github', 'v1', 'demowebs')
def delete_fn(spec, **kwargs):
    name = kwargs["body"]["metadata"]["name"] + "-deployment"
    namespace = kwargs["body"]["metadata"]["namespace"]
    # Delete the deployment spec
    # Actually delete an object by requesting the Kubernetes API.
    api = kubernetes.client.AppsV1Api()
    try:
      depl = api.delete_namespaced_deployment(name=name, namespace=namespace)
    except ApiException as e:
      print("Exception when calling AppsV1Api->delete_namespaced_deployment: %s\n" % e)

    name = kwargs["body"]["metadata"]["name"] + "-svc"
    namespace = kwargs["body"]["metadata"]["namespace"]

    # Actually delete an object by requesting the Kubernetes API.
    api = kubernetes.client.CoreV1Api()
    try:
      svc = api.delete_namespaced_service(name=name, namespace=namespace)
    except ApiException as e:
      print("Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)
