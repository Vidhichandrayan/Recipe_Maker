import streamlit as st
import requests

BACKEND_URL = None  # backend not connected yet

st.set_page_config(page_title="Smart Recipe Explorer", layout="centered")

st.title("🍽️ Smart Recipe Explorer")
st.caption("AI-powered recipe generation with full CRUD")

# -------------------------------
# Session state
# -------------------------------
if "preview_recipe" not in st.session_state:
    st.session_state.preview_recipe = None
    st.session_state.preview_ingredients = None

def backend_available():
    return BACKEND_URL is not None

# -------------------------------
# Generate (Preview Only)
# -------------------------------
st.subheader("✨ Generate Recipe")

ingredients_input = st.text_input(
    "Enter ingredients (space-separated)",
    placeholder="paneer tomato onion"
)

if st.button("Generate Recipe"):
    if not ingredients_input.strip():
        st.warning("Enter ingredients first")
    elif not backend_available():
        st.info("Backend not connected yet. Frontend is live.")
    else:
        res = requests.post(
            f"{BACKEND_URL}/generate-recipe-preview",
            json=ingredients_input.split()
        )
        if res.status_code == 200:
            st.session_state.preview_recipe = res.json()["recipe"]
            st.session_state.preview_ingredients = ingredients_input

# -------------------------------
# Preview Section
# -------------------------------
if st.session_state.preview_recipe:
    st.divider()
    st.subheader("🧾 Recipe Preview")
    st.markdown(st.session_state.preview_recipe)

# -------------------------------
# Saved Recipes Section
# -------------------------------
st.divider()
st.subheader("📚 Saved Recipes")

if not backend_available():
    st.info("Saved recipes will appear once backend is connected.")
else:
    saved = requests.get(f"{BACKEND_URL}/recipes")
    if saved.status_code == 200:
        st.write(saved.json())
