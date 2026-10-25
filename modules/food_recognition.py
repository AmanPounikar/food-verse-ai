"""
Tab 1: Food Recognition & Nutrition Audit (Epic 2).
Handles dish recognition, nutritional breakdown, macro charts, allergen alerts, and health scores.
"""

import streamlit as st
from PIL import Image
import json
from modules.sample_data import create_sample_dish_image
from modules.ui_components import render_macro_donut_chart, render_provider_badge

def render_food_recognition_tab(ai_engine):
    st.markdown("### 🥗 Food Recognition & Nutritional Audit")
    st.caption("Epic 2 • Multimodal Computer Vision Food Identification, Macro Breakdown, and Clinical Health Scoring")

    col_input, col_display = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown("#### 1. Upload or Select Dish")
        source_mode = st.radio(
            "Image Source",
            ["Upload My Own Photo", "Select High-Fidelity Sample Dish"],
            horizontal=True,
            key="dish_source_mode"
        )

        selected_image = None
        dish_notes = ""

        if source_mode == "Upload My Own Photo":
            uploaded_file = st.file_uploader(
                "Upload meal photo (JPEG, PNG, WEBP)",
                type=["jpg", "jpeg", "png", "webp"],
                key="dish_uploader"
            )
            if uploaded_file:
                selected_image = Image.open(uploaded_file)
        else:
            sample_choice = st.selectbox(
                "Preset Sample Meals",
                [
                    "Mediterranean Wild Salmon & Quinoa Bowl",
                    "Artisanal Avocado Toast with Poached Egg",
                    "Paneer Tikka Masala with Naan"
                ],
                key="sample_dish_choice"
            )
            if "Salmon" in sample_choice:
                selected_image = create_sample_dish_image("salmon_bowl")
            elif "Avocado" in sample_choice:
                selected_image = create_sample_dish_image("avocado_toast")
            else:
                selected_image = create_sample_dish_image("paneer_tikka")

        dish_notes = st.text_input(
            "Optional Notes (e.g. 'home cooked with olive oil', 'restaurant portion')",
            placeholder="e.g. Gluten-free, light on dressing...",
            key="dish_notes_input"
        )

        analyze_btn = st.button("🔍 Run Multimodal Nutrition Audit", type="primary", use_container_width=True)

    with col_display:
        st.markdown("#### 2. Visual Preview")
        if selected_image:
            st.image(selected_image, caption="Active Meal Subject", use_container_width=True)
        else:
            st.info("👆 Upload a dish photo or select a sample dish above to preview.")

    # Execution and Results
    if analyze_btn and selected_image:
        with st.spinner("🤖 Analyzing dish composition, recognizing ingredients, and calculating clinical macros..."):
            audit_result = ai_engine.analyze_dish(selected_image, dish_notes)
            st.session_state["dish_audit_result"] = audit_result

    # Display Results if present
    if "dish_audit_result" in st.session_state and st.session_state["dish_audit_result"]:
        res = st.session_state["dish_audit_result"]
        st.markdown("---")
        
        # Provider Badge
        render_provider_badge(res.get("_provider", "demo"), res.get("_model", ""))

        # Top Header Section: Dish Name & Health Score
        header_col1, header_col2, header_col3 = st.columns([2.5, 1, 1])
        with header_col1:
            st.subheader(f"🍽️ {res.get('dish_name', 'Recognized Dish')}")
            st.markdown(f"**Cuisine Origin:** {res.get('cuisine_type', 'International')} | **Portion Size:** {res.get('estimated_portion', 'Standard Serving')}")
        
        with header_col2:
            score = res.get('health_score', 85)
            grade = res.get('health_grade', 'A')
            st.metric(label="Health Score", value=f"{score}/100", delta=f"Grade {grade}")

        with header_col3:
            kcal = res.get('nutrition_breakdown', {}).get('calories_kcal', 0)
            st.metric(label="Total Energy", value=f"{kcal} kcal")

        # Health Rationale
        if res.get('health_score_rationale'):
            st.info(f"💡 **Dietitian Health Rationale:** {res.get('health_score_rationale')}")

        # Core Metrics Bar
        nutr = res.get('nutrition_breakdown', {})
        m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)
        m_col1.metric("Protein", f"{nutr.get('protein_g', 0)}g")
        m_col2.metric("Carbohydrates", f"{nutr.get('carbohydrates_g', 0)}g")
        m_col3.metric("Total Fats", f"{nutr.get('fats_g', 0)}g")
        m_col4.metric("Dietary Fiber", f"{nutr.get('dietary_fiber_g', 0)}g")
        m_col5.metric("Sugars", f"{nutr.get('sugars_g', 0)}g")
        m_col6.metric("Sodium", f"{nutr.get('sodium_mg', 0)}mg")

        # Visual Macro Chart & Ingredients
        chart_col, ing_col = st.columns([1, 1], gap="medium")

        with chart_col:
            st.markdown("##### 📊 Caloric Macronutrient Distribution")
            donut_fig = render_macro_donut_chart(
                protein_g=nutr.get('protein_g', 20),
                carbs_g=nutr.get('carbohydrates_g', 40),
                fats_g=nutr.get('fats_g', 15)
            )
            st.plotly_chart(donut_fig, use_container_width=True)

            # Caloric Burn Equivalent
            burn = res.get('caloric_burn_equivalents', {})
            if burn:
                st.markdown("##### 🏃 Caloric Burn Equivalents")
                b1, b2, b3 = st.columns(3)
                b1.caption(f"🏃 Running: **{burn.get('running_min', 45)} min**")
                b2.caption(f"🚴 Cycling: **{burn.get('cycling_min', 60)} min**")
                b3.caption(f"🚶 Walking: **{burn.get('walking_min', 100)} min**")

        with ing_col:
            st.markdown("##### 🥑 Detected Ingredients & Portions")
            ingredients = res.get('ingredients_detected', [])
            if ingredients:
                for ing in ingredients:
                    st.markdown(f"- **{ing.get('name', 'Ingredient')}**: `{ing.get('amount', 'N/A')}` *(AI Confidence: {ing.get('confidence', '95%')})*")
            else:
                st.write("Standard culinary base ingredients detected.")

            # Allergen Alerts
            st.markdown("##### ⚠️ Allergen & Sensitivity Warnings")
            allergens = res.get('allergen_alerts', [])
            if allergens:
                for a in allergens:
                    sev = a.get('severity', 'Moderate').lower()
                    sev_class = "danger" if "high" in sev else ("warning" if "med" in sev or "mod" in sev else "info")
                    st.markdown(
                        f"""<div class="fv-card" style="padding:8px 12px; margin-bottom:6px; border-left: 4px solid {'#EF4444' if sev_class=='danger' else '#F59E0B'};">
                            <strong>⚠️ {a.get('allergen', 'Allergen')} ({a.get('severity', 'Alert')})</strong><br>
                            <span style="font-size:0.85rem; color:#94A3B8;">Source: {a.get('source', 'Dish component')}</span>
                        </div>""",
                        unsafe_allow_html=True
                    )
            else:
                st.success("✅ No common major allergens flagged.")

        if res.get('clinical_dietary_notes'):
            st.markdown(f"**Clinical Dietary Note:** {res.get('clinical_dietary_notes')}")

        # JSON Export
        with st.expander("📄 Export Nutritional Audit (JSON)"):
            st.json(res)
            st.download_button(
                "📥 Download Nutritional Report (JSON)",
                data=json.dumps(res, indent=2),
                file_name=f"nutrition_audit_{res.get('dish_name', 'meal').lower().replace(' ', '_')}.json",
                mime="application/json"
            )
