import streamlit as st
import requests

API = "https://recipe-maker-1-5xzf.onrender.com"

st.set_page_config(page_title="Smart Recipe Explorer", layout="wide")
st.title("🍳 Smart Recipe Explorer")

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
                else:
                    data = r.json()
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

                        if s.status_code == 200:
                            st.success("Recipe saved")
                        else:
                            st.error(s.text)

with tab2:
    st.subheader("Saved Recipes")

    if st.button("Load Recipes"):
        r = requests.get(f"{API}/recipes")

        if r.status_code != 200:
            st.error("Failed to load")
        else:
            recipes = r.json()

            if not recipes:
                st.info("No recipes yet")
            else:
                for rec in recipes:
                    with st.expander(rec["name"]):
                        st.markdown("**Ingredients**")
                        st.write(rec["ingredients"])
                        st.markdown("**Instructions**")
                        st.write(rec["instructions"])
