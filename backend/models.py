from sqlalchemy import Column, Integer, String, Text
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    ingredients = Column(String, nullable=False)
    content = Column(Text, nullable=False)
