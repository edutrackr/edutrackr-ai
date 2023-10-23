import sys
import os
import uvicorn
from fastapi import FastAPI
from common.utils import has_arg
from config import AppConfig
from api.routes import router


project_root = os.getcwd()
sys.path.append(project_root)

app = FastAPI(
    title="Edutrackr AI",
    description="AI Engine for Edutrackr",
)
app.include_router(router)

if __name__ == "__main__":
    reload = AppConfig.IS_DEV and has_arg("--watch")
    uvicorn.run(
        'main:app',
        port=AppConfig.PORT, 
        reload=reload,
    )
