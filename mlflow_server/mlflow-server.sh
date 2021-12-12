export $(cat $(eval echo "~rainforest")/Repositories/research-devops/mlflow_server/.env | xargs)
export MLFLOW_TRACKING_PORT=$PORT
export MLFLOW_TRACKING_URI=http://$IP:$MLFLOW_TRACKING_PORT
export MLFLOW_BACKEND_STORE_URI=postgresql://mlflow:mlflow@localhost/mlflow
export MLFLOW_S3_ENDPOINT_URL=http://$IP:9000
export AWS_ACCESS_KEY_ID=$ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY
export PATH=$(eval echo "~rainforest")/Repositories/research-devops/mlflow_server/.venv/bin/:$PATH

$(eval echo "~rainforest")/Repositories/research-devops/mlflow_server/.venv/bin/mlflow server --backend-store-uri $MLFLOW_BACKEND_STORE_URI --default-artifact-root s3://mlflow -h 0.0.0.0 -p $MLFLOW_TRACKING_PORT