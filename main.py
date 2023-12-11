import logging
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, Response, status
from api.common.exceptions import AppException
from api.models.base import BaseResponse, EmptyResponse
from config import AppConfig
from api.routes.app import router
from api.common.constants.runtime import RuntimeArgs
from api.common.utils.runtime import has_arg


logger = logging.getLogger(__name__)

app = FastAPI(
    title=AppConfig.Swagger.TITLE,
    description=AppConfig.Swagger.DESCRIPTION,
    version=AppConfig.Swagger.VERSION,
)
app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, ex: RequestValidationError):
    logger.error(f"Validation error: {ex}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(BaseResponse(
            success=False, 
            message="Validation error",
            data=ex.errors()
        ))
    )

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, ex: AppException):
    logger.error(f"App error: {ex}")
    return JSONResponse(
        status_code=ex.status_code,
        content=jsonable_encoder(EmptyResponse(
            success=False,
            message=ex.description
        ))
    )

if __name__ == "__main__":
    reload = AppConfig.IS_DEV and has_arg(RuntimeArgs.WATCH_MODE)
    uvicorn.run(
        'main:app',
        port=AppConfig.PORT, 
        reload=reload,
    )
