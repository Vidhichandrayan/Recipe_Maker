from pydantic import BaseModel

class RecipeCreate(BaseModel):
    ingredients: list[str]
    content: str

class RecipeOut(BaseModel):
    id: int
    ingredients: str
    content: str

    class Config:
        orm_mode = True
