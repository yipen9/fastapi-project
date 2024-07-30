from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException  
from fastapi.responses import JSONResponse
from schemas import ResponseModel
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError

async def validate_error_exception_handler(request, exc: Exception):
    isValidationError = isinstance(exec, ValidationError) or \
          isinstance(exc, RequestValidationError) or isinstance(exc, ValueError)
    if isValidationError:
        details = []
        for error in exc.errors():
            if len(error['loc']) > 1 :
                loc = error['loc'][-1]
            else:
                loc = error['loc'][0]
            type = error['type']
            msg = error['msg'].split(',')[-1].strip()
            details.append(f"【{loc}】：{msg}")
    error_msg = ",".join(details)
    response = ResponseModel(success=False,code=400,message=error_msg)
    return JSONResponse(content=response.model_dump())


async def http_exception_handler(request: Request, exc: HTTPException):  
    response =  ResponseModel(success=False,code=exc.status_code,message=exc.detail)
    return JSONResponse(content=response.model_dump())


async def default_exception_handler(request: Request, exc: Exception):  
    response = ResponseModel(success=False,code=500,message=f"服务内部异常:{str(exc)}")
    return JSONResponse(content=response.model_dump())