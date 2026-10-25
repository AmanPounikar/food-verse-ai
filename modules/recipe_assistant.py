"""
Tab 4: Smart Kitchen Recipe Assistant (Epic 4).
Pantry inventory parser, creative culinary synthesis, cooking times,
difficulty ratings, step-by-step instructions, and intelligent ingredient substitutions.
"""

import streamlit as st
import json
from modules.ui_components import render_provider_badge

COMMON_PANTRY_ITEMS = [
    "Eggs", "Olive Oil", "Garlic", "Onions", "Tomatoes",
    "Chicken Breast", "Canned Black Beans", "Rolled Oats",
    "Spinach", "Quinoa", "Greek Yogurt", "Cheddar Cheese",
    "Soy Sauce", "Lemons", "Bell Peppers", "Tofu"
]

def render_recipe_assistant_tab(ai_engine):
    st.markdown("### 👨‍🍳 Smart Kitchen Recipe Assistant")
    st.caption("Epic 4 • Zero-Waste Pantry Synthesis, Adaptive Ingredient Substitution, and Nutritional Culinary Direction")

    col_pantry, col_filters = st.columns([1.4, 1], gap="medium")

    with col_pantry:
        st.markdown("#### 1. Available Pantry & Fridge Inventory")
        
        # Multiselect with pre-populated common staples
        default_items = ["Eggs", "Spinach", "Garlic", "Olive Oil", "Tomatoes"]
        selected_staples = st.multiselect(
            "Quick-Select Pantry Staples",
            options=COMMON_PANTRY_ITEMS,
            default=default_items,
            key="pantry_multiselect"
        )

        custom_items_text = st.text_input(
            "Add Custom Ingredients (comma-separated)",
            placeholder="e.g. Feta cheese, sourdough bread, walnuts, mushrooms",
            key="custom_pantry_text"
        )

        # Merge ingredients
        custom_list = [item.strip() for item in custom_items_text.split(",") if item.strip()]
        all_ingredients = list(dict.fromkeys(selected_staples + custom_list))

        st.caption(f"🧺 Active Pantry Inventory: **{len(all_ingredients)} items** ({', '.join(all_ingredients) if all_ingredients else 'None'})")

    with col_filters:
        st.markdown("#### 2. Cooking Constraints & Preferences")
        dietary_pref = st.selectbox(
            "Dietary Lifestyle",
            ["High Protein / Fitness", "Low Carb / Keto Friendly", "Vegetarian / Plant-Forward", "Mediterranean", "Gluten-Free", "No Restriction"],
            key="recipe_dietary_pref"
        )

        max_time = st.slider("Max Total Time (Minutes)", min_value=15, max_value=60, value=25, step=5, key="recipe_max_time")

        equipment = st.multiselect(
            "Available Equipment",
            ["Stovetop / Skillet", "Oven / Roasting Tray", "Air Fryer", "Blender / Food Processor", "Instant Pot / Pressure Cooker"],
            default=["Stovetop / Skillet", "Oven / Roasting Tray"],
            key="recipe_equipment"
        )

    generate_btn = st.button("🍳 Synthesize Creative Recipes from Pantry", type="primary", use_container_width=True)

    # Execution
    if generate_btn:
        if not all_ingredients:
            st.warning("⚠️ Please select or type at least one pantry ingredient!")
        else:
            with st.spinner("👩‍🍳 Analyzing flavor affinities, balancing macronutrients, and drafting culinary recipes..."):
                recipe_result = ai_engine.generate_smart_recipes(all_ingredients, dietary_pref, max_time, equipment)
                st.session_state["recipe_synth_result"] = recipe_result

    # Display Results
    if "recipe_synth_result" in st.session_state and st.session_state["recipe_synth_result"]:
        res = st.session_state["recipe_synth_result"]
        st.markdown("---")
        render_provider_badge(res.get("_provider", "demo"), res.get("_model", ""))

        recipes = res.get("recipes", [])
        if recipes:
            for idx, r in enumerate(recipes):
                with st.container():
                    st.markdown(f"### 🍲 Recipe {idx + 1}: {r.get('recipe_title', 'Curated Dish')}")
                    st.markdown(f"**Cuisine Vibe:** `{r.get('cuisine_style', 'Home Bistro')}` | **Difficulty:** `{r.get('difficulty', 'Easy')}` | **Servings:** `{r.get('servings', 2)}`")

                    # Time & Macro Banner
                    t1, t2, t3, t4, t5 = st.columns(5)
                    t1.metric("Prep Time", f"{r.get('prep_time_min', 10)}m")
                    t2.metric("Cook Time", f"{r.get('cook_time_min', 15)}m")
                    t3.metric("Calories", f"{r.get('calories_per_serving', 350)} kcal")
                    macros = r.get("macros", {})
                    t4.metric("Protein", f"{macros.get('protein_g', 20)}g")
                    t5.metric("Fiber", f"{macros.get('fiber_g', 5)}g")

                    # Ingredients & Step by Step
                    r_col1, r_col2 = st.columns([1, 1.3], gap="medium")

                    with r_col1:
                        st.markdown("##### 🛒 Pantry Ingredients Used")
                        for u_ing in r.get("pantry_ingredients_used", []):
                            st.markdown(f"- ✅ **{u_ing}**")

                        opt_ing = r.get("missing_or_optional_ingredients", [])
                        if opt_ing:
                            st.markdown("##### 🧂 Optional Flavor Boosters")
                            for o_ing in opt_ing:
                                st.markdown(f"- ➕ *{o_ing}*")

                        # Smart Substitutions
                        st.markdown("##### 🔄 Smart Substitutions")
                        subs = r.get("smart_substitutions", [])
                        if subs:
                            for s in subs:
                                st.markdown(
                                    f"""<div class="fv-card" style="padding:10px 12px; margin-bottom:8px; border-left:3px solid #10B981;">
                                        <strong>Swap {s.get('original', 'Item')}:</strong> Use <em>{s.get('substitution', 'Alternative')}</em><br>
                                        <span style="font-size:0.82rem; color:#94A3B8;">Chef Note: {s.get('culinary_note', 'Equal ratio swap')}</span>
                                    </div>""",
                                    unsafe_allow_html=True
                                )

                    with r_col2:
                        st.markdown("##### 📝 Step-by-Step Cooking Method")
                        steps = r.get("step_by_step_instructions", [])
                        for s_num, step in enumerate(steps, 1):
                            st.markdown(
                                f"""<div class="step-item">
                                    <div class="step-num">{s_num}</div>
                                    <div>{step}</div>
                                </div>""",
                                unsafe_allow_html=True
                            )

                        # Chef Pro Tip
                        if r.get("chef_pro_tip"):
                            st.markdown(
                                f"""<div style="background:rgba(245, 158, 11, 0.12); border:1px solid rgba(245, 158, 11, 0.35); border-radius:10px; padding:12px 16px; margin-top:12px;">
                                    <strong style="color:#FBBF24;">🌟 Executive Chef Secret:</strong><br>
                                    <span style="color:#F8FAFC; font-size:0.92rem;">{r.get('chef_pro_tip')}</span>
                                </div>""",
                                unsafe_allow_html=True
                            )

                    st.markdown("---")

            # JSON Export
            with st.expander("📄 Export Recipes (JSON)"):
                st.json(res)
                st.download_button(
                    "📥 Download Recipes JSON",
                    data=json.dumps(res, indent=2),
                    file_name="pantry_synthesized_recipes.json",
                    mime="application/json"
                )
