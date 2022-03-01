## TODO

- [ ] Containerized MLflow Server

## MLflow Setup

### [Arkade](https://github.com/alexellis/arkade) - The Open Source Kubernetes Marketplace

> [Two year update: Building an Open Source Marketplace for Kubernetes](https://blog.alexellis.io/kubernetes-marketplace-two-year-update/)

```bash
curl -sLS https://get.arkade.dev | sudo sh
```

### [Minio](https://min.io)

```bash
arkade install minio --help
```

```
Install minio

Usage:
  arkade install minio [flags]

Examples:
  arkade install minio

Flags:
      --access-key string   Provide an access key to override the pre-generated value
      --distributed         Deploy Minio in Distributed Mode
  -h, --help                help for minio
      --namespace string    Kubernetes namespace for the application (default "default")
      --persistence         Enable persistence
      --secret-key string   Provide a secret key to override the pre-generated value
      --set stringArray     Use custom flags or override existing flags
                            (example --set persistence.enabled=true)
      --update-repo         Update the helm repo (default true)

Global Flags:
      --kubeconfig string   Local path for your kubeconfig file
      --wait                If we should wait for the resource to be ready before returning (helm3 only, default false)
```

```
Info for app: minio
# Forward the minio port to your machine
kubectl port-forward -n default svc/minio 9000:9000 &

# Get the access and secret key to gain access to minio
ACCESSKEY=$(kubectl get secret -n default minio -o jsonpath="{.data.accesskey}" | base64 --decode; echo)
SECRETKEY=$(kubectl get secret -n default minio -o jsonpath="{.data.secretkey}" | base64 --decode; echo)

# Get the Minio Client
arkade get mc

# Add a host
mc config host add minio http://127.0.0.1:9000 $ACCESSKEY $SECRETKEY

# List buckets
mc ls minio
```

- Create Minio with PersistentVolume
  - About Creation of PV, please refer to [rainforest-devops](https://github.com/rainforest-tools/rainforest-devops/blob/29a2c1e3d1843a4cb7f7f2d10a59dfa057e14f2d/volumes/README.md)
    ```bash
    ark install minio --set persistence.enabled=true \
                      --set persistence.existingClaim=[PVC NAME] \
                      --update-repo --namespace minio
    ```
- Export Port for External Access
  ```bash
  kubectl patch svc {{ SERVICE NAME }} -p '{"spec":{"externalIPs":[ {{ EXTERNAL IP }} ]}}'
  ```

### Setup MLflow Server

- Prepare Environment
  ```bash
  poetry install
  ```
- Config Environment Variables
  ```bash
  # .env
  PORT=                 # External Port
  IP=                   # External Ip
  ACCESS_KEY_ID=        # ACCESSKEY for Minio
  SECRET_ACCESS_KEY=    # SECRETKEY for Minio
  ```
- `$HOME/.aws/credentials`
  ```
  [default]
  aws_access_key_id=      # ACCESSKEY for Minio
  aws_secret_access_key=  # SECRETKEY for Minio
  ```
- Create System Service
  ```
  sudo ln -s {{ PATH TO }}/mlflow-tracking.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable mlflow-tracking
  sudo systemctl start mlflow-tracking
  ```
