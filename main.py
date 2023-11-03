import uvicorn
from fastapi import FastAPI
from config import AppConfig
from api.routes import router
from api.common.constants.runtime import RuntimeArgs
from api.common.utils.runtime import has_arg


app = FastAPI(
    title="Edutrackr AI",
    description="AI Engine for Edutrackr",
    version="1.0.0"
)
app.include_router(router)

if __name__ == "__main__":
    reload = AppConfig.IS_DEV and has_arg(RuntimeArgs.WATCH_MODE)
    uvicorn.run(
        'main:app',
        port=AppConfig.PORT, 
        reload=reload,
    )
