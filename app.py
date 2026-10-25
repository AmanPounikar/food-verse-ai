"""
Food Verse AI - Multimodal Food Intelligence Agent
Skill Wallet Capstone Project 3
Production-ready Streamlit Application.
"""

import os
import streamlit as st
from modules.ui_components import apply_custom_css, render_hero_banner
from modules.ai_engine import FoodVerseAIEngine
from modules.food_recognition import render_food_recognition_tab
from modules.freshness_diagnostic import render_freshness_tab
from modules.kitchen_hygiene import render_kitchen_hygiene_tab
from modules.recipe_assistant import render_recipe_assistant_tab
from modules.meal_planner import render_meal_planner_tab

# =============================================================================
# Streamlit Application Configuration
# =============================================================================
st.set_page_config(
    page_title="Food Verse AI - Multimodal Food Intelligence Agent",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Modern Vibrant Styling
apply_custom_css()

# =============================================================================
# Sidebar Configuration & Persona Controls
# =============================================================================
with st.sidebar:
    st.markdown("### 🥑 Food Verse AI")
    st.caption("Multimodal Food Intelligence & AI Systems Agent")
    st.markdown("---")

    st.markdown("#### ⚙️ System Configuration")
    
    # Provider Selection
    provider_option = st.selectbox(
        "AI Intelligence Provider",
        [
            "Interactive Demo Mode (No Key Needed)",
            "Google Gemini (Multimodal Vision)",
            "Groq AI (Ultra-Fast Vision/LLM)"
        ],
        index=0,
        help="Select your AI inference engine. Demo Mode provides full offline food science simulations."
    )

    api_key = ""
    model_name = ""

    if "Gemini" in provider_option:
        provider = "gemini"
        default_gemini_key = os.getenv("GEMINI_API_KEY", "")
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            default_gemini_key = st.secrets["GEMINI_API_KEY"]
            
        api_key = st.text_input(
            "Gemini API Key",
            value=default_gemini_key,
            type="password",
            placeholder="AIzaSy...",
            help="Get your key at https://aistudio.google.com"
        )
        model_name = st.selectbox(
            "Gemini Model",
            ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"],
            index=0
        )
        if not api_key:
            st.warning("⚠️ No API key provided. Falling back to Standalone Demo Mode.")
            provider = "demo"

    elif "Groq" in provider_option:
        provider = "groq"
        default_groq_key = os.getenv("GROQ_API_KEY", "")
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            default_groq_key = st.secrets["GROQ_API_KEY"]

        api_key = st.text_input(
            "Groq API Key",
            value=default_groq_key,
            type="password",
            placeholder="gsk_...",
            help="Get your key at https://console.groq.com"
        )
        model_name = st.selectbox(
            "Groq Model",
            ["llama-3.2-11b-vision-preview", "llama-3.3-70b-versatile"],
            index=0
        )
        if not api_key:
            st.warning("⚠️ No API key provided. Falling back to Standalone Demo Mode.")
            provider = "demo"
    else:
        provider = "demo"
        st.success("✅ Standalone Demo Mode Active. Pre-loaded with high-fidelity scientific datasets and preset multimodal samples.")

    st.markdown("---")
    st.markdown("#### 🎯 Capstone Modules")
    st.markdown("""
    - **Tab 1 (Epic 2):** Dish Recognition & Nutrition
    - **Tab 2 (Epic 3):** Freshness & Spoilage
    - **Tab 3 (Epic 4):** Kitchen Hygiene (HACCP)
    - **Tab 4 (Epic 4):** Smart Recipe Assistant
    - **Tab 5 (Epic 5):** Precision Meal Planner
    """)

    st.markdown("---")
    if st.button("🔄 Reset Session State", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.caption("Developed for Skill Wallet Capstone Project 3 • Food Science & AI Engineering")

# =============================================================================
# Initialize AI Engine
# =============================================================================
ai_engine = FoodVerseAIEngine(
    provider=provider,
    api_key=api_key,
    model_name=model_name
)

# =============================================================================
# Main Application Flow
# =============================================================================
render_hero_banner()

# Navigation Tabs across FoodVerse Core Pillars
tabs = st.tabs([
    "🥗 1. Nutrition Audit (Epic 2)",
    "🔬 2. Freshness Diagnostic (Epic 3)",
    "🧑‍🍳 3. Kitchen Hygiene & HACCP (Epic 4)",
    "👨‍🍳 4. Smart Recipe Assistant (Epic 4)",
    "🧬 5. Personalized Meal Planner (Epic 5)"
])

with tabs[0]:
    render_food_recognition_tab(ai_engine)

with tabs[1]:
    render_freshness_tab(ai_engine)

with tabs[2]:
    render_kitchen_hygiene_tab(ai_engine)

with tabs[3]:
    render_recipe_assistant_tab(ai_engine)

with tabs[4]:
    render_meal_planner_tab(ai_engine)
