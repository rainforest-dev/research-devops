import pytest
from PIL import Image
import numpy as np
import base64
import requests


@pytest.mark.api
def test_predict():
  res = requests.post('http://localhost:8000/predict/strength',
                      files={'file': open('./000101001162163164.npy', 'rb')})
  print(res.text)