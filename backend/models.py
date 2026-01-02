from sqlalchemy import Column, Integer, String, Boolean, Text
from backend.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cuisine = Column(String)
    isVegetarian = Column(Boolean)
    prepTimeMinutes = Column(Integer)
    ingredients = Column(Text)
    instructions = Column(Text)
    difficulty = Column(String)
    tags = Column(Text)
