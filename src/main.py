import time
import yaml
import logging
import logging.config
import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title='Fastapi Project',version='1.0.0',docs_url='/api/docs',redoc_url='/api/redoc')

script_dir = os.path.dirname(os.path.abspath(__file__))
logging_file = os.path.join(script_dir,'logging.yaml')

logger = logging.getLogger(__name__)


def load_logging_config():
    with open(logging_file, 'r',encoding='utf-8') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
load_logging_config()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0',port=8000,workers=1)

