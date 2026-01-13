import streamlit as st
import requests

API = "https://recipe-maker-1-5xzf.onrender.com"

st.set_page_config(page_title="Smart Recipe Explorer", layout="wide")
st.title("🍳 Smart Recipe Explorer")

# Initialize session state for the generated recipe
if 'generated_recipe' not in st.session_state:
    st.session_state.generated_recipe = None

# Allow overriding the API URL from the UI for local testing
API = st.sidebar.text_input("API base URL", API)
st.sidebar.caption("Use this to point the app at a local backend during development")

tab1, tab2 = st.tabs(["AI Generator", "Saved Recipes"])

with tab1:
    ingredients = st.text_input("Enter ingredients (comma-separated)")

    if st.button("Generate Recipe"):
        if not ingredients:
            st.warning("Enter ingredients")
        else:
            with st.spinner("Generating..."):
                r = requests.post(
                    f"{API}/generate-recipe",
                    json={"ingredients": ingredients}
                )

                if r.status_code != 200:
                    st.error("Recipe generation failed")
                    st.session_state.generated_recipe = None
                else:
                    data = r.json()
                    st.session_state.generated_recipe = data

    # Display the generated recipe if it exists in session state
    if st.session_state.generated_recipe:
        data = st.session_state.generated_recipe
        
        st.subheader(data["name"])

        st.markdown("### Ingredients")
        st.write(data["ingredients"])

        st.markdown("### Instructions")
        st.write(data["instructions"])

        if st.button("💾 Save Recipe"):
            payload = {
                "name": data["name"],
                "cuisine": "Other",
                "isVegetarian": False,
                "prepTimeMinutes": 30,
                "ingredients": data["ingredients"],
                "instructions": data["instructions"],
                "difficulty": "Medium",
                "tags": ["ai-generated"]
            }

            s = requests.post(f"{API}/recipes", json=payload)

            if s.status_code != 200:
                st.error(f"Recipe save failed: {s.status_code} — {s.text}")
            else:
                saved = s.json()
                st.success("Recipe saved ✅")
                st.write(saved)

                # Immediately reload recipes to verify persistence
                r_reload = requests.get(f"{API}/recipes")
                if r_reload.status_code == 200:
                    st.info("Reloaded recipes from server")
                    recipes = r_reload.json()
                    st.write(f"Total saved recipes: {len(recipes)}")
                else:
                    st.warning(f"Failed to reload recipes: {r_reload.status_code}")

with tab2:
    st.subheader("Saved Recipes")

    if st.button("Load Recipes"):
        r = requests.get(f"{API}/recipes")

        if r.status_code != 200:
            st.error(f"Failed to load recipes: {r.status_code} — {r.text}")
        else:
            recipes = r.json()

            if not recipes:
                st.info("No recipes yet")
            else:
                st.success(f"Loaded {len(recipes)} recipes")
                for rec in recipes:
                    with st.expander(rec["name"]):
                        st.markdown("**Ingredients**")
                        st.write(rec["ingredients"])
                        st.markdown("**Instructions**")
                        st.write(rec["instructions"])