import streamlit as st
import requests

# Public Render backend
API = "https://recipe-maker-1-5xzf.onrender.com"

st.set_page_config(page_title="Smart Recipe Explorer", layout="wide")

st.title("🍳 Smart Recipe Explorer")

tab1, tab2 = st.tabs(["AI Generator", "Saved Recipes"])

# ---------------------------
# AI Generator Tab
# ---------------------------
with tab1:
    ingredients = st.text_input("Enter ingredients (comma-separated)")

    if st.button("Generate Recipe"):
        if ingredients.strip() == "":
            st.warning("Please enter ingredients")
        else:
            with st.spinner("Generating recipe..."):
                try:
                    res = requests.post(
                        f"{API}/generate",
                        json={"ingredients": ingredients},
                        timeout=30
                    )

                    if res.status_code == 200:
                        data = res.json()

                        st.subheader(data["title"])
                        st.markdown("### Ingredients")
                        st.write(data["ingredients"])
                        st.markdown("### Instructions")
                        st.write(data["instructions"])

                        if st.button("💾 Save Recipe"):
                            save = requests.post(
                                f"{API}/recipes",
                                json=data,
                                timeout=30
                            )
                            if save.status_code == 200:
                                st.success("Recipe saved successfully!")
                            else:
                                st.error("Failed to save recipe")

                    else:
                        st.error("Recipe generation failed")

                except:
                    st.error("Backend is waking up. Try again in 10 seconds.")

# ---------------------------
# Saved Recipes Tab
# ---------------------------
with tab2:
    st.subheader("📦 Saved Recipes")

    if st.button("Load Saved Recipes"):
        try:
            res = requests.get(f"{API}/recipes", timeout=30)

            if res.status_code == 200:
                recipes = res.json()

                if len(recipes) == 0:
                    st.info("No recipes saved yet")
                else:
                    for r in recipes:
                        with st.expander(r["title"]):
                            st.markdown("**Ingredients**")
                            st.write(r["ingredients"])
                            st.markdown("**Instructions**")
                            st.write(r["instructions"])
            else:
                st.error("Failed to fetch recipes")

        except:
            st.error("Backend is waking up. Click again in a few seconds.")
