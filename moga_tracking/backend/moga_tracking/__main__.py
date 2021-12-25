import logging
import os
import random
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from moga_tracking.utils import is_float
import numpy as np
from research_data.utils import paramToImg
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse
from PIL import Image
import tempfile
from research_utils.sqlite.functional import create_connection, query
from research_utils.sqlite.row_factory import dict_factory
from research_utils.sqlite.typing.operator import AND, Lower, SQLArgumentFactory, Upper

load_dotenv()

app = FastAPI(title='MOGA Tracking')


@app.get('/about')
def about():
  return 'tracking and visualizing results of Multi-objective Genetic Algorithm on Mlflow'


@app.get('/db/{table}/')
async def db(table: str, fields: str, vf: str):
  fields = [item for item in fields.split('-')]
  where = Lower('total_area', 0.25)
  if vf is not None:
    vf = tuple([float(item) if is_float(item) else None for item in vf.split('-')])
    lower, upper = vf
    if lower and upper:
      where = AND(
          where, SQLArgumentFactory.between('volume_fraction', lower_bound=lower,
                                            upper_bound=upper))
    elif not lower and upper:
      where = AND(where, Lower('volume_fraction', upper))
    elif not upper and lower:
      where = AND(where, Upper('volume_fraction', lower))
  conn = create_connection(os.getenv('DB_PATH'))
  rows = query(conn, table_name=table, fields=fields, row_factory=dict_factory, where=where)
  return rows


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


# TODO: disable temperately
# @app.websocket('/ws')
# async def websocket_endpoint(websocket: WebSocket):
#   logging.info('Accepting client connection...')
#   await websocket.accept()
#   while True:
#     try:
#       await websocket.receive_text()
#       resp = {'value': random.uniform(0, 1)}
#       await websocket.send_json(resp)
#     except Exception as err:
#       logging.error(err)
#       break