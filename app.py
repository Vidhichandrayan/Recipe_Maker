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
        with st.spinner("Waking up AI server and generating recipe..."):
            try:
                # Wake up backend (Render free tier sleeps)
                requests.get(f"{API}/", timeout=30)
                time.sleep(2)

                # Generate recipe
                res = requests.post(
                    f"{API}/generate-recipe",
                    json={"ingredients": ingredients},
                    timeout=120
                )

                if res.status_code == 200:
                    data = res.json()

                    st.success("Recipe generated!")

                    st.subheader(data["name"])

                    st.markdown("### 🥕 Ingredients")
                    for i in data["ingredients"]:
                        st.write(f"- {i}")

                    st.markdown("### 👨‍🍳 Instructions")
                    for idx, step in enumerate(data["instructions"], 1):
                        st.write(f"{idx}. {step}")

                    # ---- SAVE TO DB ----
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
                            st.success("Recipe saved!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to save recipe")

                else:
                    st.error("Backend error:")
                    st.code(res.text)

            except:
                st.error("Backend is waking up. Please wait 30 seconds and try again.")

# ---------------- SAVED RECIPES (CRUD) ----------------
st.markdown("---")
st.markdown("## 📚 Saved Recipes")

try:
    recipes = requests.get(f"{API}/recipes", timeout=30).json()

    if recipes:
        for r in recipes:
            with st.container():
                st.markdown(f"### {r['name']}")
                st.write(f"🍽 Cuisine: {r['cuisine']}")
                st.write(f"⏱ Prep Time: {r['prepTimeMinutes']} minutes")
                st.write(f"🥗 Vegetarian: {'Yes' if r['isVegetarian'] else 'No'}")
                st.write(f"🔥 Difficulty: {r['difficulty']}")
                st.write("🧂 Ingredients:", ", ".join(r["ingredients"]))
                st.write("🏷 Tags:", ", ".join(r["tags"]))

                if st.button(f"🗑 Delete {r['id']}"):
                    requests.delete(f"{API}/recipes/{r['id']}")
                    st.success("Deleted!")
                    time.sleep(1)
                    st.rerun()
    else:
        st.info("No saved recipes yet.")

except:
    st.warning("Could not load saved recipes.")
