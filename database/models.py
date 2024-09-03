from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Relationship
from database.database_config import Base

class Skin(Base):
    __tablename__ = "skins"

    name = Column(String, primary_key=True)
    number = Column(Integer, nullable=False)
    image = Column(String, nullable=False)

    champion_name = Column(String, ForeignKey("champions.name"), primary_key=True)
    champion = Relationship("Champion", back_populates="skins")

class Champion(Base):
    __tablename__ = "champions"

    name = Column(String, primary_key=True)
    role = Column(String)
    
    skins = Relationship("Skin", order_by=Skin.name, back_populates="champion")