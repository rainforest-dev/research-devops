import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from mlflow.tracking import MlflowClient
from mlflow.pytorch import load_model
import torch
import torchvision.transforms.functional as F
from torchinfo.torchinfo import summary
import mlflow
from research.utils.util import import_from_path
from research.utils.mlflow import load_state_dict, classifier_builder
from research.data_preprocessing.transforms import TorchScaler
from hydra import compose, initialize, initialize_config_dir
from hydra.utils import instantiate

load_dotenv()

app = FastAPI(title='MLflow Model Serve')

origins = ["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

client = MlflowClient()
models = {}


@app.get('/about')
def about():
  return 'APIs for strength and toughness prediction via image regression'


@app.post('/predict/{model_name}/{model_version}')
async def predict(model_name: str, model_version: int, file: UploadFile = File(...)):
  img = np.load(file.file)

  model = f'{model_name}/{model_version}'
  model_uri = f'models:/{model}'
  dst_path = f'models/{model}'

  os.makedirs(dst_path, exist_ok=True)

  if model not in models:
    models[model] = load_model(model_uri=model_uri,
                               map_location=torch.device('cpu'),
                               dst_path=dst_path)

  img = torch.unsqueeze(F.to_tensor(img), 0)
  y_hat = models[model](img)
  return {'data': y_hat.detach().numpy().flatten().tolist()}


@app.post('/predict/{run_id}')
async def predict(run_id: str, file: UploadFile = File(...), inverse: bool = True):
  img = np.load(file.file)

  if run_id not in models:
    model = load_state_dict(client=client, run_id=run_id)
    model.eval()
    models[run_id] = model

  img = torch.unsqueeze(F.to_tensor(img), 0)
  y_hat = models[run_id](img)
  y_hat = y_hat.detach().numpy().flatten().tolist()

  if inverse:
    return {'data': transform(run_id=run_id, value=y_hat, inverse=inverse)}
  return {'data': y_hat}

@app.post('/classify/{run_id}')
async def classify(run_id: str, file: UploadFile = File(...), threshold: float = 0.5):
  img = np.load(file.file)

  if run_id not in models:
    model = load_state_dict(client=client, run_id=run_id, model_builder=classifier_builder)
    model.eval()
    models[run_id] = model

  img = torch.unsqueeze(F.to_tensor(img), 0)
  y_hat = models[run_id](img)
  y_hat = y_hat.detach().numpy()
  y_hat = np.where(y_hat >= threshold, True, False)
  y_hat = y_hat.flatten().tolist()
  return {'data': y_hat }


@app.post('/classify/v2/{run_id}')
async def classify_v2(run_id: str, file: UploadFile = File(...), threshold: float = 0.5):
  img = np.load(file.file)

  if run_id not in models:
    # [reference](https://stackoverflow.com/questions/70991020/how-to-reload-hydra-config-with-enumerations)
    from hydra.core.global_hydra import GlobalHydra
    from hydra.core.config_store import ConfigStore
    from research.hydra.dataclass import Config, ModelConfig
    cs = ConfigStore.instance()
    cs.store(name="base_config", node=Config)
    cs.store(group="model", name="base_classifier", node=ModelConfig)
    cs = ConfigStore.instance()
    cs.store(
        name="reload_config",
        node={
            "defaults": [
                "base_config",
                "config",
            ]
        },
    )
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dst_path = Path('models', run_id, 'state_dict/')
    os.makedirs(dst_path, exist_ok=True)
    local_path = client.download_artifacts(run_id, 'state_dict', dst_path)
    state_dict = mlflow.pytorch.load_state_dict(local_path, map_location=device)
    config_path = client.download_artifacts(run_id, 'output/.hydra', dst_path)
    GlobalHydra.instance().clear()
    initialize_config_dir(config_dir=config_path)
    config = compose("reload_config")
    model = instantiate(config.model, _recursive_=False)
    model.load_state_dict(dict(state_dict['model']), strict=False)
    model.eval()
    print(config_path, model)
    models[run_id] = model

  img = torch.unsqueeze(F.to_tensor(img), 0)
  y_hat = models[run_id](img)
  y_hat = y_hat.detach().numpy()
  y_hat = np.where(y_hat >= threshold, True, False)
  y_hat = y_hat.flatten().tolist()
  return {'data': y_hat }

def scaler_builder(state_dict: dict, args: dict, local_path: str, config_path: str):
  scaler = args.get('scaler')()
  scaler.load_state_dict(dict(state_dict['scaler']), strict=False)
  return scaler


def transform(run_id: str, value: List[float] = [], inverse: bool = False):
  key = f'{run_id}_scaler'
  if key not in models:
    model: TorchScaler = load_state_dict(client=client, run_id=run_id, model_builder=scaler_builder)
    model.eval()
    models[key] = model
  if inverse:
    return models[key].inverse_transform([value]).squeeze(0).tolist()
  else:
    return models[key].transform([value]).squeeze(0).tolist()


@app.post('/scaler/{run_id}')
async def normalize(run_id: str, value: List[float] = [], inverse: bool = False):
  return {'data': transform(run_id=run_id, value=value, inverse=inverse)}
