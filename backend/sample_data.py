from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Recipe
import uuid

def generate_recipe_id():
    """Generate unique recipe ID"""
    return f"rec_{uuid.uuid4().hex[:8]}"

def seed_database():
    """Populate database with sample recipes"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(Recipe).count() > 0:
        print("Database already contains recipes. Skipping seed.")
        db.close()
        return
    
    sample_recipes = [
        {
            "id": generate_recipe_id(),
            "name": "Paneer Butter Masala",
            "cuisine": "Indian",
            "is_vegetarian": True,
            "prep_time_minutes": 40,
            "ingredients": ["paneer", "tomato", "cream", "butter", "spices", "onion", "garlic", "ginger"],
            "difficulty": "medium",
            "instructions": "Step 1: Heat butter in a pan. Step 2: Add onions and sauté until golden. Step 3: Add ginger-garlic paste and cook. Step 4: Add tomato puree and spices. Step 5: Add paneer cubes and cream. Step 6: Simmer for 10 minutes and serve hot.",
            "tags": ["dinner", "party", "rich", "popular"]
        },
        {
            "id": generate_recipe_id(),
            "name": "Dal Tadka",
            "cuisine": "Indian",
            "is_vegetarian": True,
            "prep_time_minutes": 30,
            "ingredients": ["lentils", "tomato", "onion", "cumin", "turmeric", "ghee", "garlic", "green chili"],
            "difficulty": "easy",
            "instructions": "Step 1: Pressure cook lentils with turmeric. Step 2: Heat ghee in a pan. Step 3: Add cumin seeds and let them crackle. Step 4: Add garlic and green chili. Step 5: Add to cooked dal and mix. Step 6: Garnish with coriander.",
            "tags": ["lunch", "healthy", "protein", "comfort food"]
        },
        {
            "id": generate_recipe_id(),
            "name": "Chicken Biryani",
            "cuisine": "Indian",
            "is_vegetarian": False,
            "prep_time_minutes": 90,
            "ingredients": ["chicken", "basmati rice", "yogurt", "onion", "spices", "saffron", "mint", "ghee"],
            "difficulty": "hard",
            "instructions": "Step 1: Marinate chicken in yogurt and spices for 2 hours. Step 2: Cook rice until 70% done. Step 3: Fry onions until golden. Step 4: Layer chicken and rice. Step 5: Add saffron milk and fried onions. Step 6: Dum cook on low heat for 30 minutes.",
            "tags": ["special", "celebration", "festive", "aromatic"]
        },
        {
            "id": generate_recipe_id(),
            "name": "Masala Dosa",
            "cuisine": "Indian",
            "is_vegetarian": True,
            "prep_time_minutes": 25,
            "ingredients": ["dosa batter", "potato", "onion", "mustard seeds", "curry leaves", "turmeric", "green chili"],
            "difficulty": "medium",
            "instructions": "Step 1: Prepare potato filling with spices. Step 2: Heat dosa pan. Step 3: Pour batter and spread thin. Step 4: Cook until crispy. Step 5: Add potato filling. Step 6: Fold and serve with chutney and sambar.",
            "tags": ["breakfast", "south indian", "crispy", "traditional"]
        },
        {
            "id": generate_recipe_id(),
            "name": "Pasta Carbonara",
            "cuisine": "Italian",
            "is_vegetarian": False,
            "prep_time_minutes": 20,
            "ingredients": ["spaghetti", "eggs", "bacon", "parmesan cheese", "black pepper", "garlic"],
            "difficulty": "easy",
            "instructions": "Step 1: Boil pasta in salted water. Step 2: Fry bacon until crispy. Step 3: Mix eggs and parmesan. Step 4: Drain pasta and add to bacon. Step 5: Remove from heat and add egg mixture. Step 6: Toss quickly and serve with pepper.",
            "tags": ["quick", "italian", "creamy", "dinner"]
        },
        {
            "id": generate_recipe_id(),
            "name": "Margherita Pizza",
            "cuisine": "Italian",
            "is_vegetarian": True,
            "prep_time_minutes": 60,
            "ingredients": ["pizza dough", "tomato sauce", "mozzarella cheese", "fresh basil", "olive oil", "garlic"],
            "difficulty": "medium",
            "instructions": "Step 1: Prepare pizza dough and let it rise. Step 2: Roll out dough into circle. Step 3: Spread tomato sauce. Step 4: Add mozzarella cheese. Step 5: Bake at 250°C for 12-15 minutes. Step 6: Top with fresh basil and olive oil.",
            "tags": ["dinner", "classic", "italian", "cheese"]
        },
        {
            "id": generate_recipe_id(),
            "name": "Pad Thai",
            "cuisine": "Thai",
            "is_vegetarian": False,
            "prep_time_minutes": 30,
            "ingredients": ["rice noodles", "shrimp", "eggs", "peanuts", "bean sprouts", "tamarind", "fish sauce", "lime"],
            "difficulty": "medium",
            "instructions": "Step 1: Soak rice noodles. Step 2: Prepare pad thai sauce. Step 3: Stir-fry shrimp. Step 4: Add noodles and sauce. Step 5: Add eggs and vegetables. Step 6: Garnish with peanuts, lime, and bean sprouts.",
            "tags": ["dinner", "asian", "noodles", "street food"]
        },
        {
            "id": generate_recipe_id(),
            "name": "Greek Salad",
            "cuisine": "Greek",
            "is_vegetarian": True,
            "prep_time_minutes": 15,
            "ingredients": ["tomato", "cucumber", "red onion", "feta cheese", "olives", "olive oil", "lemon", "oregano"],
            "difficulty": "easy",
            "instructions": "Step 1: Chop tomatoes and cucumbers into chunks. Step 2: Slice red onions. Step 3: Add feta cheese and olives. Step 4: Make dressing with olive oil, lemon, and oregano. Step 5: Toss everything together. Step 6: Serve fresh.",
            "tags": ["healthy", "lunch", "salad", "fresh", "quick"]
        },
        {
            "id": generate_recipe_id(),
            "name": "Chocolate Chip Cookies",
            "cuisine": "American",
            "is_vegetarian": True,
            "prep_time_minutes": 45,
            "ingredients": ["flour", "butter", "sugar", "chocolate chips", "eggs", "vanilla extract", "baking soda", "salt"],
            "difficulty": "easy",
            "instructions": "Step 1: Cream butter and sugar. Step 2: Add eggs and vanilla. Step 3: Mix in dry ingredients. Step 4: Fold in chocolate chips. Step 5: Drop spoonfuls on baking sheet. Step 6: Bake at 180°C for 10-12 minutes.",
            "tags": ["dessert", "baking", "sweet", "snack"]
        },
        {
            "id": generate_recipe_id(),
            "name": "Vegetable Stir Fry",
            "cuisine": "Chinese",
            "is_vegetarian": True,
            "prep_time_minutes": 20,
            "ingredients": ["mixed vegetables", "soy sauce", "garlic", "ginger", "sesame oil", "cornstarch", "vegetable oil"],
            "difficulty": "easy",
            "instructions": "Step 1: Chop all vegetables uniformly. Step 2: Heat oil in wok. Step 3: Add garlic and ginger. Step 4: Stir-fry vegetables on high heat. Step 5: Add soy sauce and cornstarch slurry. Step 6: Toss and serve hot with rice.",
            "tags": ["healthy", "quick", "vegan", "dinner", "asian"]
        }
    ]
    
    for recipe_data in sample_recipes:
        recipe = Recipe(**recipe_data)
        db.add(recipe)
    
    db.commit()
    print(f"Successfully seeded {len(sample_recipes)} recipes into the database!")
    db.close()

if __name__ == "__main__":
    seed_database()