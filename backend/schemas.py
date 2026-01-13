from pydantic import BaseModel
from typing import List

class RecipeCreate(BaseModel):
    name: str
    cuisine: str
    isVegetarian: bool
    prepTimeMinutes: int
    ingredients: List[str]
    instructions: List[str]
    difficulty: str
    tags: List[str]
