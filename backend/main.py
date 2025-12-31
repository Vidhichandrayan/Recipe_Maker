from fastapi import FastAPI
from .database import engine, Base
from .ai_service import generate_recipe
from .crud import save_recipe, get_all_recipes, delete_recipe, update_recipe

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Recipe Explorer")

@app.get("/")
def root():
    return {"message": "Smart Recipe Explorer running 🚀"}

# 🔹 Generate ONLY (no save)
@app.post("/generate-recipe-preview")
def generate_recipe_preview(ingredients: list[str]):
    recipe_text = generate_recipe(ingredients)
    return {"recipe": recipe_text}

# 🔹 Save explicitly
@app.post("/save-recipe")
def save_recipe_api(payload: dict):
    ingredients = payload["ingredients"]
    content = payload["content"]
    saved = save_recipe(ingredients, content)
    return {"id": saved.id, "message": "Recipe saved"}

# 🔹 Read
@app.get("/recipes")
def read_recipes():
    return get_all_recipes()

# 🔹 Delete
@app.delete("/recipes/{recipe_id}")
def remove_recipe(recipe_id: int):
    delete_recipe(recipe_id)
    return {"message": "Recipe deleted"}

# 🔹 Update
@app.put("/recipes/{recipe_id}")
def edit_recipe(recipe_id: int, payload: dict):
    updated = update_recipe(recipe_id, payload["content"])
    return {"message": "Recipe updated", "recipe": updated}
