import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form, Request
import numpy as np
from mlflow.tracking import MlflowClient
from mlflow.pytorch import load_model
import torch
import torchvision.transforms.functional as F
from torchinfo.torchinfo import summary
from research.utils.util import import_from_path
from research.utils.mlflow import load_state_dict, classifier_builder
from research.data_preprocessing.transforms import TorchScaler

load_dotenv()

app = FastAPI()
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
