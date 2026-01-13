import streamlit as st
import requests

# 🔥 This MUST be your deployed FastAPI URL (Render)
API = "https://recipe-maker-1-5xzf.onrender.com"

st.set_page_config(page_title="Smart Recipe Explorer", layout="wide")

st.title("🍳 Smart Recipe Explorer")

tab1, tab2 = st.tabs(["AI Generator", "Saved Recipes"])

# -------------------------------
# TAB 1 — Generate Recipe
# -------------------------------
with tab1:
    ingredients = st.text_input("Enter ingredients (comma-separated)")

    if st.button("Generate Recipe"):
        if ingredients.strip() == "":
            st.warning("Please enter ingredients")
        else:
            with st.spinner("Generating recipe..."):
                try:
                    response = requests.post(
                        f"{API}/generate",
                        json={"ingredients": ingredients}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.subheader(data["title"])
                        st.write("### Ingredients")
                        st.write(data["ingredients"])
                        st.write("### Instructions")
                        st.write(data["instructions"])

                        if st.button("💾 Save Recipe"):
                            save_res = requests.post(
                                f"{API}/recipes",
                                json=data
                            )

                            if save_res.status_code == 200:
                                st.success("Recipe saved successfully!")
                            else:
                                st.error("Failed to save recipe")

                    else:
                        st.error("Recipe generation failed")

                except Exception as e:
                    st.error("Backend is not reachable. Check API deployment.")

# -------------------------------
# TAB 2 — Saved Recipes
# -------------------------------
with tab2:
    st.subheader("📦 Saved Recipes")

    try:
        res = requests.get(f"{API}/recipes")

        if res.status_code == 200:
            recipes = res.json()

            if len(recipes) == 0:
                st.info("No saved recipes yet")
            else:
                for r in recipes:
                    with st.expander(r["title"]):
                        st.write("### Ingredients")
                        st.write(r["ingredients"])
                        st.write("### Instructions")
                        st.write(r["instructions"])
        else:
            st.error("Failed to fetch recipes")

    except:
        st.error("Cannot connect to backend server")
