import streamlit as st
import requests
import time

API = "https://recipe-maker-1-5xzf.onrender.com"

st.set_page_config(page_title="Smart Recipe Explorer", layout="centered")

st.title("🍳 Smart Recipe Explorer")

# ---------------- AI GENERATION ----------------
ingredients = st.text_input("Enter ingredients (comma-separated)")

if st.button("Generate Recipe"):
    if not ingredients.strip():
        st.warning("Please enter ingredients")
    else:
        with st.spinner("Generating recipe using AI..."):
            try:
                # Wake Render backend
                requests.get(f"{API}/", timeout=30)
                time.sleep(2)

                res = requests.post(
                    f"{API}/generate-recipe",
                    json={"ingredients": ingredients},
                    timeout=120
                )

                if res.status_code == 200:
                    data = res.json()

                    st.subheader(data["name"])

                    st.markdown("### 🥕 Ingredients")
                    for i in data["ingredients"]:
                        st.write(f"- {i}")

                    st.markdown("### 👨‍🍳 Instructions")
                    for idx, step in enumerate(data["instructions"], 1):
                        st.write(f"{idx}. {step}")

                    # SAVE TO DATABASE
                    if st.button("💾 Save Recipe"):
                        payload = {
                            "name": data["name"],
                            "cuisine": "AI Generated",
                            "isVegetarian": True,
                            "prepTimeMinutes": 15,
                            "ingredients": data["ingredients"],
                            "instructions": data["instructions"],
                            "difficulty": "Medium",
                            "tags": ["ai", "generated"]
                        }

                        save = requests.post(f"{API}/recipes", json=payload)

                        if save.status_code == 200:
                            st.cache_data.clear()   # 🔥 force refresh
                            st.success("Recipe saved!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(save.text)

                else:
                    st.error("AI backend error")

            except Exception:
                st.error("Backend is waking up. Please try again in 20 seconds.")

# ---------------- SAVED RECIPES ----------------
st.markdown("---")
st.markdown("## 📚 Saved Recipes")

@st.cache_data(ttl=10)
def load_recipes():
    return requests.get(f"{API}/recipes").json()

try:
    recipes = load_recipes()

    if recipes:
        for r in recipes:
            st.markdown(f"### {r['name']}")
            st.write("Ingredients:", ", ".join(r["ingredients"]))
            st.write("Difficulty:", r["difficulty"])

            if st.button(f"🗑 Delete {r['id']}"):
                requests.delete(f"{API}/recipes/{r['id']}")
                st.cache_data.clear()
                st.rerun()
    else:
        st.info("No saved recipes yet.")

except:
    st.warning("Could not load recipes.")
