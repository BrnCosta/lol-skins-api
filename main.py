import uvicorn
from fastapi import FastAPI

from logger import logger
from services.ddragon_service import DDragonService

app = FastAPI()
ddragon_service = DDragonService()

@app.get("/")
def root():
    return {"message": "Root!"}

@app.get("/latest-version")
def version():
    return ddragon_service.get_latest_package_version()

@app.get("/champions-list")
def champions():
    return ddragon_service.get_champions_list()

if __name__ == "__main__":
    logger.info("Starting the FastAPI application")
    uvicorn.run(app, host="0.0.0.0", port=8000)