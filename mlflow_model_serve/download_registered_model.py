import os, shutil
from argparse import ArgumentParser
from dotenv import load_dotenv
import mlflow
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository

if __name__ == '__main__':
  load_dotenv()
  parser = ArgumentParser()
  parser.add_argument('--name', '-n', help='model name')
  parser.add_argument('--version', '-v', type=int, help='model version')
  args = parser.parse_args()
  model_name = args.name
  model_version = args.version
  dst_path = 'model'

  if os.path.exists(dst_path):
    shutil.rmtree(dst_path)
  os.makedirs(dst_path, exist_ok=True)
  local_path = ModelsArtifactRepository(f'models:/{model_name}/{model_version}').download_artifacts(
      '', dst_path=dst_path)
  print(f'Model {model_name}, version {model_version} is downloaded at {local_path}')