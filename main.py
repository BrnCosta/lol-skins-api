import uvicorn
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from logger import logger
from services import ddragon_service
from database.database_config import engine, get_db
from database.models import Champion, Base

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def startup_event(app: FastAPI):
    logger.info("Starting the FastAPI application. Initiating DDragon information...")
    await ddragon_service.initiate_ddragon_information()
    yield
    logger.info("Finishing API...")

app = FastAPI(lifespan=startup_event)

@app.get("/")
def root():
    return {"message": "Root!"}

@app.get("/latest-version")
def version():
    return ddragon_service.get_latest_package_version()

@app.get("/champions-list")
def champions():
    return ddragon_service.get_champions_list()

@app.get("/champion/{champion_name}")
async def get_champion(champion_name, db: Session = Depends(get_db)):
    champion = db.query(Champion).filter(Champion.name == champion_name).first()
    return champion

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)