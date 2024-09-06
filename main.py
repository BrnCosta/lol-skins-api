import uvicorn
from fastapi import FastAPI, Depends

from contextlib import asynccontextmanager

from logger import logger
from services import ddragon_service, champion_service, skin_service

from database.database_config import engine, get_db
from database.models import Base

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def startup_event(app: FastAPI):
    logger.info("Starting the FastAPI application. Initiating DDragon information...")
    await ddragon_service.initiate_ddragon_information()
    yield
    logger.info("Finishing API...")

app = FastAPI(lifespan=startup_event)

@app.get("/version")
def version():
    return ddragon_service.get_latest_package_version()

@app.get("/champions")
async def champions(db = Depends(get_db)):
    return await champion_service.get_all_champions(db)

@app.get("/champions/{champion_name}")
async def get_champion(champion_name, db = Depends(get_db)):
    return await champion_service.get_champion_by_name(champion_name, db)

@app.get("/skins")
async def skins(db = Depends(get_db)):
    return await skin_service.get_all_skins(db)

@app.get("/skins/{skin_name}")
async def get_skin(skin_name, db = Depends(get_db)):
    return await skin_service.get_skin_by_name(skin_name, db)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)