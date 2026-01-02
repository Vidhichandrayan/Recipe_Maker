import json
import random
import requests
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine
from backend import models, crud, schemas

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Recipe Explorer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def call_mistral(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.9}
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=90)
    r.raise_for_status()
    return r.json().get("response", "")

@app.post("/generate-recipe")
def generate_recipe(req: dict):
    ingredients = req.get("ingredients", "")
    seed = random.randint(1, 99999)

    prompt = f"""
Create a UNIQUE recipe using: {ingredients}.
Variation ID: {seed}

Return ONLY valid JSON:
{{
  "name": "Recipe name",
  "ingredients": ["item1", "item2"],
  "instructions": ["step1", "step2"]
}}
"""

    try:
        raw = call_mistral(prompt)
        try:
            return json.loads(raw)
        except:
            start, end = raw.find("{"), raw.rfind("}")
            return json.loads(raw[start:end+1])
    except:
        return {
            "name": "Fallback Recipe",
            "ingredients": ingredients.split(","),
            "instructions": ["Prepare", "Cook", "Serve"]
        }

@app.post("/recipes")
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_recipe(db, recipe)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/recipes")
def get_recipes(db: Session = Depends(get_db)):
    recipes = crud.get_all_recipes(db)
    return [
        {
            "id": r.id,
            "name": r.name,
            "cuisine": r.cuisine,
            "isVegetarian": r.isVegetarian,
            "prepTimeMinutes": r.prepTimeMinutes,
            "ingredients": r.ingredients.split(","),
            "instructions": r.instructions,
            "difficulty": r.difficulty,
            "tags": r.tags.split(","),
        }
        for r in recipes
    ]

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = crud.delete_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Deleted"}
