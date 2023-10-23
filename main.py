import sys
import os
import uvicorn
from fastapi import FastAPI
from api.routes import router
from config import AppConfig

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, port=AppConfig.PORT)
