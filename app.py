import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config("Smart Recipe Explorer", "🍳")
st.title("🍳 Smart Recipe Explorer")

if "recipe" not in st.session_state:
    st.session_state.recipe = None

tab1, tab2 = st.tabs(["🤖 AI Generator", "📦 Saved Recipes"])

with tab1:
    ingredients = st.text_input("Enter ingredients (comma-separated)")

    if st.button("Generate Recipe"):
        res = requests.post(f"{API}/generate-recipe", json={"ingredients": ingredients})
        st.session_state.recipe = res.json()

    if st.session_state.recipe:
        r = st.session_state.recipe
        st.subheader(r["name"])

        for i in r["ingredients"]:
            st.write("-", i)

        for s in r["instructions"]:
            st.write("•", s)

        if st.button("💾 Save Recipe"):
            payload = {
                "name": str(r["name"]),
                "cuisine": "AI Generated",
                "isVegetarian": True,
                "prepTimeMinutes": 30,
                "ingredients": [str(i) for i in r["ingredients"]],
                "instructions": " ".join(r["instructions"]),
                "difficulty": "medium",
                "tags": ["ai", "generated"]
            }

            resp = requests.post(f"{API}/recipes", json=payload)
            if resp.status_code in [200, 201]:
                st.success("✅ Recipe saved")
            else:
                st.error("❌ Save failed")
                st.code(resp.text)

with tab2:
    recipes = requests.get(f"{API}/recipes").json()

    if not recipes:
        st.info("No recipes saved")

    for r in recipes:
        with st.expander(r["name"]):
            st.write(", ".join(r["ingredients"]))
            if st.button(f"Delete {r['id']}"):
                requests.delete(f"{API}/recipes/{r['id']}")
                st.experimental_rerun()
