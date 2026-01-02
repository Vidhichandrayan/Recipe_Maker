import streamlit as st
import requests

#BACKEND_URL = "https://YOUR-RENDER-URL.onrender.com"
BACKEND_URL = "https://smart-recipe-explorer-demo.onrender.com"

st.set_page_config("Smart Recipe Explorer", "🍳")
st.title("🍳 Smart Recipe Explorer (Demo)")

if "recipe" not in st.session_state:
    st.session_state.recipe = None

tab1, tab2 = st.tabs(["🤖 AI Generator", "📦 Saved Recipes"])

# ---------- AI GENERATOR ----------
with tab1:
    ingredients = st.text_input("Enter ingredients (comma-separated)")

    if st.button("Generate Recipe"):
        res = requests.post(
            f"{BACKEND_URL}/generate-recipe",
            json={"ingredients": ingredients},
            timeout=60
        )
        st.session_state.recipe = res.json()

    if st.session_state.recipe:
        r = st.session_state.recipe
        st.subheader(r["name"])

        st.write("### Ingredients")
        for i in r["ingredients"]:
            st.write("-", i)

        st.write("### Instructions")
        for step in r["instructions"]:
            st.write("•", step)

        if st.button("💾 Save Recipe"):
            payload = {
                "name": r["name"],
                "cuisine": "AI Generated",
                "isVegetarian": True,
                "prepTimeMinutes": 30,
                "ingredients": r["ingredients"],
                "instructions": " ".join(r["instructions"]),
                "difficulty": "medium",
                "tags": ["demo", "ai"]
            }
            resp = requests.post(f"{BACKEND_URL}/recipes", json=payload)
            if resp.status_code == 200:
                st.success("Recipe saved!")

# ---------- SAVED RECIPES ----------
with tab2:
    try:
        recipes = requests.get(f"{BACKEND_URL}/recipes").json()
    except:
        recipes = []

    if not recipes:
        st.info("No saved recipes yet")

    for r in recipes:
        with st.expander(r["name"]):
            st.write(", ".join(r["ingredients"]))
            if st.button(f"Delete {r['id']}"):
                requests.delete(f"{BACKEND_URL}/recipes/{r['id']}")
                st.experimental_rerun()
