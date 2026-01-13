import streamlit as st
import requests

API = "https://recipe-maker-1-5xzf.onrender.com"

st.set_page_config(page_title="Smart Recipe Explorer", layout="wide")
st.title("🍳 Smart Recipe Explorer")

tab1, tab2 = st.tabs(["AI Generator", "Saved Recipes"])

with tab1:
    ingredients = st.text_input("Enter ingredients (comma-separated)")

    if st.button("Generate Recipe"):
        if ingredients.strip() == "":
            st.warning("Please enter ingredients")
        else:
            try:
                res = requests.post(
                    f"{API}/generate-recipe",
                    json={"ingredients": ingredients},
                    timeout=30
                )

                if res.status_code == 200:
                    data = res.json()

                    st.subheader(data["name"])
                    st.write(data["ingredients"])
                    st.write(data["instructions"])

                    if st.button("💾 Save Recipe"):
                        payload = {
                            "name": data["name"],
                            "ingredients": "\n".join(data["ingredients"]),
                            "instructions": "\n".join(data["instructions"])
                        }

                        save = requests.post(
                            f"{API}/recipes",
                            json=payload,
                            timeout=30
                        )

                        if save.status_code == 200:
                            st.success("Recipe saved")
                        else:
                            st.error("Save failed")

                else:
                    st.error("Recipe generation failed")

            except Exception as e:
                st.error("Backend waking up. Try again.")

with tab2:
    if st.button("Load Saved Recipes"):
        try:
            res = requests.get(f"{API}/recipes", timeout=30)

            if res.status_code == 200:
                recipes = res.json()

                if len(recipes) == 0:
                    st.info("No recipes yet")
                else:
                    for r in recipes:
                        with st.expander(r["name"]):
                            st.write(r["ingredients"])
                            st.write(r["instructions"])
            else:
                st.error("Failed to fetch recipes")

        except:
            st.error("Backend waking up. Try again.")
