from database.models import Champion, Skin
from sqlalchemy.orm import Session
from sqlalchemy import select, update

async def get_all_skins(db: Session):
    query = select(Skin)\
        .join(Champion.skins)\
        .where(Skin.name != 'default')\
        .order_by(Skin.champion_name)
    
    skins = db.execute(query)
    return skins.mappings().all()

async def set_skin_owned_status(skin_id: str, owned: bool, db: Session):
    skin = db.get(Skin, skin_id)

    if not skin:
        return {"error": "Skin not found!"}
    
    skin.owned = owned
    db.commit()

async def get_skin_by_name(skin_name, db: Session):
    skin = db.query(Skin)\
                 .filter(Skin.name.ilike(skin_name))\
                 .first()
    
    if not skin:
        return {"error": "Skin not found!"}

    return {
        "id": skin.id,
        "name": skin.name,
        "owned": skin.owned,
        "champion": skin.champion_name
    }