import logging
import os
import random
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Query
from moga_tracking.utils import is_float
from research_utils.sqlite.functional import create_connection, query
from research_utils.sqlite.row_factory import dict_factory
from research_utils.sqlite.typing.operator import AND, Lower, SQLArgumentFactory, Upper, Equal
from .routers import mlflow, nacre

load_dotenv()

app = FastAPI(title='MOGA Tracking')

origins = ["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(mlflow.router)
app.include_router(nacre.router)


@app.get('/about')
def about():
  return 'tracking and visualizing results of Multi-objective Genetic Algorithm on Mlflow'


@app.get('/db/{table}/')
async def db(table: str,
             fields: str,
             vf: str,
             total_area: float = 0.25,
             num: Optional[int] = Query(None)):
  fields = [item for item in fields.split('-')]
  where = Lower('total_area', total_area)
  if vf is not None:
    vf = tuple(
        [float(item) if is_float(item) else None for item in vf.split('-')])
    lower, upper = vf
    if lower and upper:
      where = AND(
          where,
          SQLArgumentFactory.between('volume_fraction',
                                     lower_bound=lower,
                                     upper_bound=upper))
    elif not lower and upper:
      where = AND(where, Lower('volume_fraction', upper))
    elif not upper and lower:
      where = AND(where, Upper('volume_fraction', lower))
  conn = create_connection(os.getenv('DB_PATH'))
  rows = query(conn,
               table_name=table,
               fields=fields,
               row_factory=dict_factory,
               where=where)
  if num is None:
    return rows
  num = min(num, len(rows))
  return random.sample(rows, num)


@app.get('/db/{table}/{id}')
async def db_item(table: str, id: str, fields: str):
  fields = [item for item in fields.split('-')]
  conn = create_connection(os.getenv('DB_PATH'))
  rows = query(conn,
               table_name=table,
               fields=fields,
               row_factory=dict_factory,
               where=Equal('id', id))
  return rows[0]


app.mount("/artifacts",
          StaticFiles(directory=os.getenv("ARTIFACTS_PATH")),
          name="artifacts")

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