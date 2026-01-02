from sqlalchemy.orm import Session
from backend import models, schemas

def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        name=recipe.name,
        cuisine=recipe.cuisine,
        isVegetarian=recipe.isVegetarian,
        prepTimeMinutes=recipe.prepTimeMinutes,
        ingredients=",".join(recipe.ingredients),
        instructions=recipe.instructions,
        difficulty=recipe.difficulty,
        tags=",".join(recipe.tags),
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_all_recipes(db: Session):
    return db.query(models.Recipe).all()

def delete_recipe(db: Session, recipe_id: int):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    return recipe
