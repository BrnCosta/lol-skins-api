from database.models import Champion, Skin
from sqlalchemy.orm import Session
from sqlalchemy import select

async def get_all_skins(db: Session):
    query = select(Skin.name, Skin.image, Skin.champion_name)\
        .join(Champion.skins)\
        .where(Skin.name != 'default')\
        .order_by(Skin.champion_name)
    
    champions = db.execute(query)
    return champions.mappings().all()

async def get_skin_by_name(skin_name, db: Session):
    skin = db.query(Skin.name, Skin.image, Skin.champion_name)\
                 .filter(Skin.name.ilike(skin_name))\
                 .first()
    
    if not skin:
        return {"error": "Skin not found!"}

    return {
        "name": skin.name,
        "image": skin.image
    }