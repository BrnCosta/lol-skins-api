from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.orm import Relationship
from database.database_config import Base

class Skin(Base):
    __tablename__ = "skins"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    owned = Column(Boolean, nullable=False, default=False)

    champion_name = Column(String, ForeignKey("champions.name"), nullable=False)
    champion = Relationship("Champion", back_populates="skins")

class Champion(Base):
    __tablename__ = "champions"

    name = Column(String, primary_key=True)
    role = Column(String)
    
    skins = Relationship("Skin", order_by=Skin.name, back_populates="champion")