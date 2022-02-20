# Backend

- .env

```
MLFLOW_TRACKING_URI=http://
MLFLOW_S3_ENDPOINT_URL=http://
DB_PATH=./research-data.sqlite
TMP=./tmp
```

## FastAPI

### Installation

```bash
pip install fastapi
pip install "uvicorn[standard]"
# with file upload support
pip install python-multipart
```

### Run

```bash
uvicorn api.main:app --reload
```

# Frontend

- .env

```
VITE_API_ENDPOINT=http://localhost:3000
```
