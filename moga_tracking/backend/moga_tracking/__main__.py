import logging
import os
import random
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
import numpy as np
from research_data.utils import paramToImg
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse
from PIL import Image
import tempfile

load_dotenv()

app = FastAPI(title='MOGA Tracking')


@app.get('/about')
def about():
  return 'tracking and visualizing results of Multi-objective Genetic Algorithm on Mlflow'


@app.get('/nacre/{params}')
async def nacre_image(background_tasks: BackgroundTasks,
                      params: str,
                      img_size: Optional[int] = 512,
                      format: str = 'jpg',
                      unit_cell: bool = False):
  params = [int(item) for item in params.split('_')]
  img = paramToImg(param=params, is_unit_cell=unit_cell, chromosome_length=img_size)
  filename = f'{"".join(str(item) for item in params)}'
  # [reference](https://stackoverflow.com/a/64717120)
  _, path = tempfile.mkstemp(suffix=f'.{format}')
  if format == 'jpg' or format == 'png':
    img = Image.fromarray(img * 255)
    img.save(path)
  elif format == 'npy':
    # !currently broken
    np.save(path, img)

  background_tasks.add_task(lambda path: os.unlink(path), path)
  return FileResponse(path=path, filename=f'{filename}.{format}')


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
  logging.info('Accepting client connection...')
  await websocket.accept()
  while True:
    try:
      await websocket.receive_text()
      resp = {'value': random.uniform(0, 1)}
      await websocket.send_json(resp)
    except Exception as err:
      logging.error(err)
      break