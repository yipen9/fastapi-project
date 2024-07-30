import time
import yaml
import logging
import logging.config
import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from  auth.router import auth_router
from goods.router import good_router
from fastapi.exceptions import RequestValidationError  
from exceptions import validate_error_exception_handler,http_exception_handler,default_exception_handler
from fastapi import Request, HTTPException 
from pydantic import ValidationError

app = FastAPI(title='Fastapi Project',version='1.0.0',docs_url='/api/docs',redoc_url='/api/redoc')

app.add_exception_handler(ValueError, validate_error_exception_handler)
app.add_exception_handler(ValidationError, validate_error_exception_handler)
app.add_exception_handler(RequestValidationError, validate_error_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, default_exception_handler)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth_router)
app.include_router(good_router)


script_dir = os.path.dirname(os.path.abspath(__file__))
logging_file = os.path.join(script_dir,'logging.yaml')

logger = logging.getLogger(__name__)


# def load_logging_config():
#     with open(logging_file, 'r',encoding='utf-8') as f:
#         config = yaml.safe_load(f.read())
#         logging.config.dictConfig(config)
# load_logging_config()

def load_logging_config():
    with open(logging_file, 'r',encoding='utf-8') as f:
        config = yaml.safe_load(f.read())
        return config

logging_conf = load_logging_config()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0',port=8000,workers=1,log_config=logging_conf,log_level='info')