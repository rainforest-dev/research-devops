from typing import Optional
import os
from dotenv import load_dotenv
import yaml
from fastapi import APIRouter
from fastapi.params import Path, Query
from mlflow.tracking import MlflowClient
from research_moga.utils import download_artifacts, glob_gens_yaml_to_dicts, params2id
from ..typing import MlflowRunInfoType

load_dotenv()

router = APIRouter(prefix='/mlflow', tags=["mlflow"])
client = MlflowClient()


@router.get('/{run_id}/{info_type}')
@router.get('/{run_id}/{info_type}/{info_key}')
def run_info(run_id: str, info_type: MlflowRunInfoType, info_key: Optional[str] = Query(None)):
  run = client.get_run(run_id=run_id)
  if info_type == MlflowRunInfoType.PARAMS:
    return run.data.params.get(info_key, run.data.params)


def transform(item: dict):
  item['id'] = params2id(item.pop('params'), seperator='_')
  return item


@router.get('/{run_id}/moga/gens/')
@router.get('/{run_id}/moga/gens/{gen_id}')
def moga_gens(run_id: str, gen_id: Optional[int] = Query(None)):
  local_path = download_artifacts(run_id=run_id,
                                  remote_path='gens',
                                  local_path=os.getenv('TMP', 'tmp'),
                                  client=client)
  if gen_id is not None:
    result = yaml.load(open(f'{local_path}/gen_{gen_id}.yml'), yaml.Loader)
    result = [transform(item) for item in result.values()]
    return result
  else:
    results = glob_gens_yaml_to_dicts(path=local_path)
    return results
