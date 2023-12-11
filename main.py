import uvicorn
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from api.common.exceptions import AppException
from config import AppConfig
from api.routes.app import router
from api.common.constants.runtime import RuntimeArgs
from api.common.utils.runtime import has_arg


app = FastAPI(
    title=AppConfig.Swagger.TITLE,
    description=AppConfig.Swagger.DESCRIPTION,
    version=AppConfig.Swagger.VERSION,
)
app.include_router(router)

@app.exception_handler(AppException)
async def unicorn_exception_handler(request: Request, ex: AppException):
    print(ex)
    return JSONResponse(
        status_code=ex.status_code,
        content={ "message": ex.description },
    )

if __name__ == "__main__":
    reload = AppConfig.IS_DEV and has_arg(RuntimeArgs.WATCH_MODE)
    uvicorn.run(
        'main:app',
        port=AppConfig.PORT, 
        reload=reload,
    )
