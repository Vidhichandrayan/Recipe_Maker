import json
import random
import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from groq import Groq

from backend.database import SessionLocal, engine
from backend import models, crud, schemas

# ---------------- CONFIG ----------------
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Recipe Explorer – Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HEALTH ----------------
@app.get("/")
def health():
    return {"status": "ok"}

# ---------------- DB DEP ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- AI GENERATION ----------------
@app.post("/generate-recipe")
def generate_recipe(req: dict):
    ingredients = req.get("ingredients", "")
    seed = random.randint(1000, 99999)

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
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )

        raw = response.choices[0].message.content.strip()

        try:
            return json.loads(raw)
        except:
            start, end = raw.find("{"), raw.rfind("}")
            return json.loads(raw[start:end + 1])

    except Exception:
        return {
            "name": "Fallback Recipe",
            "ingredients": ingredients.split(","),
            "instructions": ["Prepare", "Cook", "Serve"]
        }

# ---------------- CRUD ----------------
@app.post("/recipes")
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)

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
            "instructions": r.instructions.split("|"),
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
