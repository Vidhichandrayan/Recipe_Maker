import streamlit as st
import requests

API = "https://recipe-maker-1-5xzf.onrender.com"

st.set_page_config(page_title="Smart Recipe Explorer", layout="wide", page_icon="🍳")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #FF6B6B 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
    }
    .recipe-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🍳 Smart Recipe Explorer</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-bottom: 2rem;'>Generate delicious recipes from your ingredients using AI</p>", unsafe_allow_html=True)

# Initialize session state for the generated recipe
if 'generated_recipe' not in st.session_state:
    st.session_state.generated_recipe = None
if 'save_success' not in st.session_state:
    st.session_state.save_success = False

tab1, tab2 = st.tabs(["🤖 AI Generator", "📚 Saved Recipes"])

with tab1:
    st.markdown("### Enter Your Ingredients")
    ingredients = st.text_input(
        "What do you have in your kitchen?",
        placeholder="e.g., chicken, tomatoes, garlic, pasta",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button("✨ Generate Recipe", type="primary", use_container_width=True)

    if generate_btn:
        if not ingredients:
            st.warning("⚠️ Please enter some ingredients first!")
        else:
            with st.spinner("🔮 Creating your perfect recipe..."):
                try:
                    r = requests.post(
                        f"{API}/generate-recipe",
                        json={"ingredients": ingredients},
                        timeout=30
                    )

                    if r.status_code != 200:
                        st.error("❌ Recipe generation failed. Please try again.")
                        st.session_state.generated_recipe = None
                    else:
                        data = r.json()
                        st.session_state.generated_recipe = data
                        st.session_state.save_success = False
                        st.success("✅ Recipe generated successfully!")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                    st.session_state.generated_recipe = None

    # Display the generated recipe if it exists in session state
    if st.session_state.generated_recipe:
        data = st.session_state.generated_recipe
        
        st.markdown("---")
        
        # Recipe Title
        st.markdown(f"## 🍽️ {data['name']}")
        
        # Two columns for ingredients and instructions
        col_ing, col_inst = st.columns([1, 1])
        
        with col_ing:
            st.markdown("### 🥗 Ingredients")
            if isinstance(data['ingredients'], list):
                for ing in data['ingredients']:
                    st.markdown(f"• {ing}")
            else:
                st.write(data['ingredients'])
        
        with col_inst:
            st.markdown("### 👨‍🍳 Instructions")
            if isinstance(data['instructions'], list):
                for idx, instruction in enumerate(data['instructions'], 1):
                    st.markdown(f"**{idx}.** {instruction}")
            else:
                st.write(data['instructions'])
        
        st.markdown("---")
        
        # Save button centered
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.save_success:
                st.success("✅ Recipe already saved!")
            else:
                if st.button("💾 Save Recipe", type="secondary", use_container_width=True):
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

                    try:
                        s = requests.post(f"{API}/recipes", json=payload, timeout=30)

                        if s.status_code != 200:
                            st.error(f"❌ Failed to save recipe. Please try again.")
                        else:
                            st.session_state.save_success = True
                            st.success("✅ Recipe saved successfully!")
                            st.balloons()
                            
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Connection error: {str(e)}")

with tab2:
    st.markdown("### 📖 Your Recipe Collection")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        load_btn = st.button("🔄 Load Recipes", type="primary", use_container_width=True)

    if load_btn:
        with st.spinner("Loading your recipes..."):
            try:
                r = requests.get(f"{API}/recipes", timeout=30)

                if r.status_code != 200:
                    st.error(f"❌ Failed to load recipes. Please try again.")
                else:
                    recipes = r.json()

                    if not recipes:
                        st.info("📝 No recipes saved yet. Generate and save your first recipe!")
                    else:
                        st.success(f"✅ Loaded {len(recipes)} recipe{'s' if len(recipes) != 1 else ''}")
                        
                        for rec in recipes:
                            with st.expander(f"🍴 {rec['name']}", expanded=False):
                                col_a, col_b = st.columns([1, 1])
                                
                                with col_a:
                                    st.markdown("**📝 Ingredients**")
                                    if isinstance(rec['ingredients'], list):
                                        for ing in rec['ingredients']:
                                            st.markdown(f"• {ing}")
                                    else:
                                        st.write(rec['ingredients'])
                                
                                with col_b:
                                    st.markdown("**👨‍🍳 Instructions**")
                                    if isinstance(rec['instructions'], list):
                                        for idx, instruction in enumerate(rec['instructions'], 1):
                                            st.markdown(f"**{idx}.** {instruction}")
                                    else:
                                        st.write(rec['instructions'])
                                
                                # Show metadata
                                st.markdown("---")
                                meta_col1, meta_col2, meta_col3 = st.columns(3)
                                with meta_col1:
                                    st.caption(f"🍽️ {rec.get('cuisine', 'N/A')}")
                                with meta_col2:
                                    st.caption(f"⏱️ {rec.get('prepTimeMinutes', 'N/A')} mins")
                                with meta_col3:
                                    st.caption(f"📊 {rec.get('difficulty', 'N/A')}")
                                    
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #999; font-size: 0.9rem;'>Made by Vidhi Chandrayan</p>", unsafe_allow_html=True)