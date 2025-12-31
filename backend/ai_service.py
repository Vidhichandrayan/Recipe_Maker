import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_recipe(ingredients: list[str]) -> str:
    prompt = f"""
    Create a detailed recipe using these ingredients:
    {', '.join(ingredients)}

    Include:
    - Recipe name
    - Ingredients
    - Step-by-step instructions
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert AI chef."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
