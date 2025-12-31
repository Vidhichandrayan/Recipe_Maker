import streamlit as st
import requests

# Backend URL from Streamlit secrets
BACKEND_URL = st.secrets.get("BACKEND_URL")

st.set_page_config(page_title="Smart Recipe Explorer", layout="centered")

st.title("🍽️ Smart Recipe Explorer")
st.caption("AI-powered recipe generation with full CRUD")

# -------------------------------
# Session state
# -------------------------------
if "preview_recipe" not in st.session_state:
    st.session_state.preview_recipe = None
    st.session_state.preview_ingredients = None

# -------------------------------
# Generate Recipe
# -------------------------------
st.subheader("✨ Generate Recipe")

ingredients_input = st.text_input(
    "Enter ingredients (space-separated)",
    placeholder="paneer tomato onion"
)

if st.button("Generate Recipe"):
    if not BACKEND_URL:
        st.error("Backend URL not configured")
    elif not ingredients_input.strip():
        st.warning("Enter ingredients first")
    else:
        try:
            res = requests.post(
                f"{BACKEND_URL}/generate-recipe-preview",
                json=ingredients_input.split(),
                timeout=15
            )
            if res.status_code == 200:
                st.session_state.preview_recipe = res.json()["recipe"]
                st.session_state.preview_ingredients = ingredients_input
            else:
                st.error("Backend error")
        except requests.exceptions.RequestException:
            st.error("Backend not reachable")

# -------------------------------
# Preview + Save
# -------------------------------
if st.session_state.preview_recipe:
    st.divider()
    st.subheader("🧾 Recipe Preview")
    st.markdown(st.session_state.preview_recipe)

    if st.button("💾 Save Recipe"):
        try:
            requests.post(
                f"{BACKEND_URL}/save-recipe",
                json={
                    "ingredients": st.session_state.preview_ingredients.split(),
                    "content": st.session_state.preview_recipe
                },
                timeout=15
            )
            st.success("Recipe saved!")
            st.session_state.preview_recipe = None
        except requests.exceptions.RequestException:
            st.error("Save failed")

# -------------------------------
# Saved Recipes
# -------------------------------
st.divider()
st.subheader("📚 Saved Recipes")

if not BACKEND_URL:
    st.info("Backend not connected")
else:
    try:
        saved = requests.get(f"{BACKEND_URL}/recipes", timeout=15)
        if saved.status_code == 200 and saved.json():
            for recipe in saved.json()[::-1]:
                st.write(recipe)
        else:
            st.info("No recipes saved yet")
    except requests.exceptions.RequestException:
        st.error("Backend not reachable")
