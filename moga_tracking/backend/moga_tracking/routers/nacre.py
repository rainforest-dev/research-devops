import os
from typing import Optional
import tempfile
from dotenv import load_dotenv
from fastapi import APIRouter
import numpy as np
from research_data.utils import paramsToImg
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse
from PIL import Image

load_dotenv()

router = APIRouter(prefix='/nacre', tags=["nacre"])


@router.get('/{params}')
async def nacre_image(background_tasks: BackgroundTasks,
                      params: str,
                      img_size: Optional[int] = 512,
                      format: str = 'jpg',
                      unit_cell: bool = False):
    """return nacre image

    Args:
        background_tasks (BackgroundTasks):
        params (str): design params
        img_size (Optional[int], optional): Defaults to 512.
        format (str, optional): Defaults to 'jpg'.
        unit_cell (bool, optional): Defaults to False.
    """
    params = [int(item) for item in params.split('_')]
    img = paramsToImg(params=params, is_unit_cell=unit_cell,
                      chromosome_length=img_size)
    filename = f'{"".join(str(item) for item in params)}'
    # [reference](https://stackoverflow.com/a/64717120)
    _, path = tempfile.mkstemp(suffix=f'.{format}')
    if format == 'jpg' or format == 'png':
        img = Image.fromarray(img * 255)
        img.save(path)
    elif format == 'npy':
        # !currently broken
        np.save(path, img)

    background_tasks.add_task(os.unlink, path)
    return FileResponse(path=path, filename=f'{filename}.{format}')


# @router.get('/design_space/')
# async def nacre_image(params: str):
#     pass
