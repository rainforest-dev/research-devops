FROM rainforest80256/pytorch-notebook-cpu:latest

USER root

RUN pip install kubeflow-kale
RUN pip install jupyterlab
RUN jupyter labextension install kubeflow-kale-launcher

ENV NB_PREFIX /

CMD ["sh","-c", "jupyter lab --notebook-dir=/home/jovyan --ip=0.0.0.0 --no-browser --allow-root --port=8888 --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*' --NotebookApp.base_url=${NB_PREFIX}"]
