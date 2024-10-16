from database.models import Champion, Skin
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

async def get_all_champions(db: Session):
    query = select(Champion.name, Skin.id.label("default-skin"))\
        .join(Champion.skins)\
        .where(Skin.name == 'default')\
        .order_by(Champion.name)
    
    champions = db.execute(query)
    
    return champions.mappings().all()

async def get_champion_by_name(champion_name, db: Session):
    champion = db.query(Champion)\
                 .options(selectinload(Champion.skins))\
                 .filter(Champion.name.ilike(champion_name))\
                 .first()
    
    if not champion:
        return {"error": "Champion not found!"}

    return {
        "name": champion.name,
        "skins": sorted([{"id": skin.id, "name": skin.name} for skin in champion.skins], 
                    key=lambda skin: int(skin['id'].split('_')[1]))
    }