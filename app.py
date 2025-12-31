import streamlit as st
import requests

# ===============================
# Backend config
# ===============================
# Backend NOT deployed yet
BACKEND_URL = None
# Later you will change this to:
# BACKEND_URL = "https://your-backend.onrender.com"

def backend_available():
    return isinstance(BACKEND_URL, str) and BACKEND_URL.startswith("http")

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
# Generate Recipe (Preview)
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
        st.info("🔌 Backend not connected yet. Frontend is live.")
    else:
        try:
            res = requests.post(
                f"{BACKEND_URL}/generate-recipe-preview",
                json=ingredients_input.split(),
                timeout=10
            )
            if res.status_code == 200:
                st.session_state.preview_recipe = res.json()["recipe"]
                st.session_state.preview_ingredients = ingredients_input
            else:
                st.error("Backend error while generating recipe")
        except Exception:
            st.error("Could not connect to backend")

# -------------------------------
# Preview Section
# -------------------------------
if st.session_state.preview_recipe:
    st.divider()
    st.subheader("🧾 Recipe Preview")
    st.markdown(st.session_state.preview_recipe)

# -------------------------------
# Saved Recipes
# -------------------------------
st.divider()
st.subheader("📚 Saved Recipes")

if not backend_available():
    st.info("Saved recipes will appear once backend is connected.")
else:
    try:
        saved = requests.get(f"{BACKEND_URL}/recipes", timeout=10)
        if saved.status_code == 200 and saved.json():
            for recipe in saved.json()[::-1]:
                st.write(recipe)
        else:
            st.info("No recipes saved yet.")
    except Exception:
        st.error("Backend unreachable")
