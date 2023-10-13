import sys
import os
from fastapi import FastAPI
from api.routes import router

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)