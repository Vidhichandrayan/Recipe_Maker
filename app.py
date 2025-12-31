import streamlit as st
import requests

BACKEND_URL = None

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
# Generate (PREVIEW ONLY)
# -------------------------------
st.subheader("✨ Generate Recipe")

ingredients_input = st.text_input(
    "Enter ingredients (space-separated)",
    placeholder="paneer tomato onion"
)

if st.button("Generate Recipe"):
    if ingredients_input.strip():
        res = requests.post(
            f"{BACKEND_URL}/generate-recipe-preview",
            json=ingredients_input.split()
        )
        if res.status_code == 200:
            st.session_state.preview_recipe = res.json()["recipe"]
            st.session_state.preview_ingredients = ingredients_input
    else:
        st.warning("Enter ingredients first")

# -------------------------------
# Preview + Save / Discard
# -------------------------------
if st.session_state.preview_recipe:
    st.divider()
    st.subheader("🧾 Recipe Preview")

    st.markdown(st.session_state.preview_recipe)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Recipe"):
            requests.post(
                f"{BACKEND_URL}/save-recipe",
                json={
                    "ingredients": st.session_state.preview_ingredients.split(),
                    "content": st.session_state.preview_recipe
                }
            )
            st.success("Recipe saved!")
            st.session_state.preview_recipe = None

    with col2:
        if st.button("❌ Discard"):
            st.session_state.preview_recipe = None
            st.info("Recipe discarded")

# -------------------------------
# Saved Recipes (READ + UPDATE + DELETE)
# -------------------------------
st.divider()
st.subheader("📚 Saved Recipes")

saved = requests.get(f"{BACKEND_URL}/recipes")

if saved.status_code == 200 and saved.json():
    for recipe in saved.json()[::-1]:
        with st.expander(f"🥗 {recipe['ingredients']}"):
            edited = st.text_area(
                "Edit recipe",
                recipe["content"],
                key=f"edit_{recipe['id']}",
                height=300
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✏️ Update", key=f"update_{recipe['id']}"):
                    requests.put(
                        f"{BACKEND_URL}/recipes/{recipe['id']}",
                        json={"content": edited}
                    )
                    st.success("Recipe updated")

            with col2:
                if st.button("🗑️ Delete", key=f"delete_{recipe['id']}"):
                    requests.delete(
                        f"{BACKEND_URL}/recipes/{recipe['id']}"
                    )
                    st.experimental_rerun()
else:
    st.info("No recipes saved yet.")
