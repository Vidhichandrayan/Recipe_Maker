from sqlalchemy.orm import Session
from database import SessionLocal
from models import Recipe

def save_recipe(ingredients: list[str], content: str):
    db: Session = SessionLocal()
    recipe = Recipe(
        ingredients=", ".join(ingredients),
        content=content
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    db.close()
    return recipe

def get_all_recipes():
    db: Session = SessionLocal()
    recipes = db.query(Recipe).all()
    db.close()
    return recipes

def delete_recipe(recipe_id: int):
    db = SessionLocal()
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    db.close()

# 🔹 UPDATE (NEW)
def update_recipe(recipe_id: int, new_content: str):
    db = SessionLocal()
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe:
        recipe.content = new_content
        db.commit()
        db.refresh(recipe)
    db.close()
    return recipe
