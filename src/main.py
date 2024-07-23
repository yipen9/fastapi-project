import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI(title='Fastapi Project',version='1.0.0',docs_url='/api/docs',redoc_url='/api/redoc')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0',port=8000,workers=1)