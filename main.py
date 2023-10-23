import sys
import os
import uvicorn
from fastapi import FastAPI
from api.routes import router
from config import AppConfig


project_root = os.getcwd()
sys.path.append(project_root)

app = FastAPI(title="Edutrackr AI Engine")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, port=AppConfig.PORT)
