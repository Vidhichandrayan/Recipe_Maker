import streamlit as st
import requests

# ================= CONFIG =================
BACKEND_URL = "https://recipe-maker-1-5xzf.onrender.com"

st.set_page_config(
    page_title="Smart Recipe Explorer",
    page_icon="🍳",
    layout="centered"
)

# ================= UI =================
st.title("🔍 Smart Recipe Explorer")

tabs = st.tabs(["🤖 AI Generator"])

with tabs[0]:
    st.subheader("Generate a Recipe")

    ingredients = st.text_input(
        "Enter ingredients (comma-separated)",
        placeholder="paneer, tomato, onion"
    )

    if st.button("Generate Recipe"):
        if not ingredients.strip():
            st.warning("Please enter some ingredients.")
        else:
            with st.spinner("Generating recipe..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate-recipe",
                        json={"ingredients": ingredients},
                        timeout=60
                    )

                    if response.status_code != 200:
                        st.error(f"Backend error: {response.text}")
                    else:
                        data = response.json()

                        # ===== DISPLAY RESULT =====
                        st.success("Recipe generated!")

                        st.markdown(f"## 🍽️ {data.get('name', 'Recipe')}")

                        st.markdown("### 🧾 Ingredients")
                        for item in data.get("ingredients", []):
                            st.write(f"- {item}")

                        st.markdown("### 👩‍🍳 Instructions")
                        for idx, step in enumerate(data.get("instructions", []), start=1):
                            st.write(f"{idx}. {step}")

                except requests.exceptions.RequestException as e:
                    st.error("Could not connect to backend. Please try again later.")
                    st.caption(str(e))
