"""
Tab 5: Personalized Meal Planner (Epic 5).
Captures biometric profile, computes BMR and TDEE via the Mifflin-St Jeor equation,
optimizes macronutrient ratios, and generates an adaptive 7-day schedule with an automated grocery list.
"""

import streamlit as st
import json
import pandas as pd
from modules.ui_components import render_macro_donut_chart, render_provider_badge

def calculate_bmr_and_tdee(gender: str, weight_kg: float, height_cm: float, age: int, activity_level: str, goal: str):
    """Computes Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE)."""
    # Mifflin-St Jeor Equation
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Activity Multipliers
    multipliers = {
        "Sedentary (desk job, minimal movement)": 1.2,
        "Lightly Active (light exercise 1-3 days/wk)": 1.375,
        "Moderately Active (moderate training 3-5 days/wk)": 1.55,
        "Very Active (hard exercise 6-7 days/wk)": 1.725,
        "Extra Active (athlete, intense twice/day)": 1.9
    }
    act_mult = multipliers.get(activity_level, 1.55)
    tdee = bmr * act_mult

    # Goal Caloric Adjustment
    if "Fat Loss" in goal:
        target_calories = max(1200, tdee - 500)
    elif "Muscle Gain" in goal:
        target_calories = tdee + 350
    elif "Aggressive Cut" in goal:
        target_calories = max(1200, tdee - 750)
    else:
        target_calories = tdee

    return bmr, tdee, target_calories


def calculate_macronutrients(target_calories: float, weight_kg: float, goal: str, dietary_pref: str):
    """Calculates macro split (protein, carbs, fat in grams and percentages)."""
    # Protein prioritization (1.8g to 2.2g per kg body weight depending on goal)
    if "Muscle" in goal or "Fat Loss" in goal:
        protein_g = min(target_calories * 0.35 / 4, weight_kg * 2.0)
    else:
        protein_g = weight_kg * 1.6

    if "Keto" in dietary_pref:
        carbs_g = 30.0 # Strict keto cap
        fats_g = (target_calories - (protein_g * 4) - (carbs_g * 4)) / 9
    elif "Diabetic" in dietary_pref or "Low Carb" in dietary_pref:
        carbs_pct = 0.30
        carbs_g = (target_calories * carbs_pct) / 4
        fats_g = (target_calories - (protein_g * 4) - (carbs_g * 4)) / 9
    else:
        # Standard balanced distribution
        fat_pct = 0.28
        fats_g = (target_calories * fat_pct) / 9
        carbs_g = (target_calories - (protein_g * 4) - (fats_g * 9)) / 4

    return {
        "protein_g": round(protein_g, 1),
        "carbs_g": round(carbs_g, 1),
        "fats_g": round(fats_g, 1)
    }


def render_meal_planner_tab(ai_engine):
    st.markdown("### 🧬 Personalized Precision Metabolic Meal Planner")
    st.caption("Epic 5 • Mifflin-St Jeor Biometric Engine, Adaptive 7-Day Macronutrient Schedule, and Consolidated Grocery Logistics")

    with st.expander("📝 Step 1: Biometric & Nutritional Profile Formulation", expanded=True):
        p_col1, p_col2, p_col3 = st.columns(3)

        with p_col1:
            age = st.number_input("Age (Years)", min_value=16, max_value=100, value=28, step=1)
            gender = st.selectbox("Biological Sex", ["Female", "Male"])
            height_cm = st.number_input("Height (cm)", min_value=120.0, max_value=230.0, value=168.0, step=0.5)

        with p_col2:
            weight_kg = st.number_input("Current Weight (kg)", min_value=35.0, max_value=250.0, value=65.0, step=0.5)
            goal = st.selectbox(
                "Primary Metabolic Goal",
                ["Fat Loss & Definition (-500 kcal)", "Muscle Hypertrophy & Strength (+350 kcal)", "Maintenance & Body Recomposition", "Aggressive Fat Loss (-750 kcal)"]
            )
            activity_level = st.selectbox(
                "Weekly Physical Activity Level",
                [
                    "Sedentary (desk job, minimal movement)",
                    "Lightly Active (light exercise 1-3 days/wk)",
                    "Moderately Active (moderate training 3-5 days/wk)",
                    "Very Active (hard exercise 6-7 days/wk)",
                    "Extra Active (athlete, intense twice/day)"
                ],
                index=2
            )

        with p_col3:
            dietary_pref = st.selectbox(
                "Clinical Dietary Constraints",
                ["Diabetic-Friendly (Low Glycemic)", "Mediterranean Longevity", "High Protein Vegan", "Vegetarian", "Keto / Ultra-Low Carb", "Pescatarian", "Standard Clean Eating"]
            )
            meals_per_day = st.selectbox("Meal Frequency", ["3 Meals + 1 Snack", "3 Large Meals", "Intermittent Fasting 16:8 (2 Meals + 1 Snack)"])
            allergies = st.text_input("Allergies / Dislikes", placeholder="e.g. Peanuts, shellfish, dairy")

    # Real-time metabolic calculation
    bmr, tdee, target_calories = calculate_bmr_and_tdee(gender, weight_kg, height_cm, age, activity_level, goal)
    macro_split = calculate_macronutrients(target_calories, weight_kg, goal, dietary_pref)

    # Metabolic Dashboard
    st.markdown("#### ⚡ Metabolic Targets Summary")
    mb_col1, mb_col2, mb_col3, mb_col4, mb_col5, mb_col6 = st.columns(6)
    mb_col1.metric("Basal Rate (BMR)", f"{int(bmr)} kcal", help="Mifflin-St Jeor resting energy expenditure")
    mb_col2.metric("Total TDEE", f"{int(tdee)} kcal", help="Total expenditure with physical activity")
    mb_col3.metric("Target Calories", f"{int(target_calories)} kcal", delta=f"{int(target_calories - tdee)} kcal")
    mb_col4.metric("Protein Target", f"{int(macro_split['protein_g'])}g")
    mb_col5.metric("Carbs Target", f"{int(macro_split['carbs_g'])}g")
    mb_col6.metric("Fats Target", f"{int(macro_split['fats_g'])}g")

    generate_plan_btn = st.button("🚀 Synthesize 7-Day Adaptive Schedule & Grocery List", type="primary", use_container_width=True)

    if generate_plan_btn:
        profile_data = {
            "age": age,
            "gender": gender,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "activity_level": activity_level,
            "goal": goal,
            "dietary_pref": dietary_pref,
            "meals_per_day": meals_per_day,
            "allergies": allergies
        }
        with st.spinner("🤖 Constructing 7-day nutrient-timed meal matrix and compiling grocery consolidation..."):
            plan_result = ai_engine.generate_meal_plan(profile_data, bmr, tdee, target_calories, macro_split)
            st.session_state["meal_plan_result"] = plan_result

    # Display Results
    if "meal_plan_result" in st.session_state and st.session_state["meal_plan_result"]:
        res = st.session_state["meal_plan_result"]
        st.markdown("---")
        render_provider_badge(res.get("_provider", "demo"), res.get("_model", ""))

        st.subheader("🗓️ Adaptive 7-Day Precision Meal Schedule")
        
        schedule = res.get("weekly_schedule", [])
        
        # Tabs for 7 days
        day_names = [d.get("day", f"Day {i+1}") for i, d in enumerate(schedule)]
        if day_names:
            day_tabs = st.tabs(day_names)
            for idx, tab in enumerate(day_tabs):
                day_data = schedule[idx]
                with tab:
                    st.markdown(f"**Daily Focus:** `{day_data.get('focus', 'Metabolic Performance')}`")
                    tot = day_data.get("daily_totals", {})
                    d1, d2, d3, d4 = st.columns(4)
                    d1.caption(f"🔥 Calories: **{tot.get('calories', int(target_calories))} kcal**")
                    d2.caption(f"🥩 Protein: **{tot.get('protein_g', int(macro_split['protein_g']))}g**")
                    d3.caption(f"🌾 Carbs: **{tot.get('carbs_g', int(macro_split['carbs_g']))}g**")
                    d4.caption(f"🥑 Fats: **{tot.get('fats_g', int(macro_split['fats_g']))}g**")

                    m_col1, m_col2 = st.columns(2)
                    with m_col1:
                        bf = day_data.get("breakfast", {})
                        st.markdown(
                            f"""<div class="fv-card" style="border-left: 4px solid #10B981;">
                                <strong style="color:#34D399;">🌅 Breakfast ({bf.get('calories', 0)} kcal | {bf.get('protein_g', 0)}g P)</strong><br>
                                <div style="font-weight:700; margin:4px 0;">{bf.get('name', 'Wholesome Breakfast')}</div>
                                <span style="font-size:0.88rem; color:#94A3B8;">{bf.get('desc', 'Nutrient-rich start')}</span>
                            </div>""",
                            unsafe_allow_html=True
                        )

                        din = day_data.get("dinner", {})
                        st.markdown(
                            f"""<div class="fv-card" style="border-left: 4px solid #3B82F6;">
                                <strong style="color:#60A5FA;">🌙 Dinner ({din.get('calories', 0)} kcal | {din.get('protein_g', 0)}g P)</strong><br>
                                <div style="font-weight:700; margin:4px 0;">{din.get('name', 'Balanced Dinner')}</div>
                                <span style="font-size:0.88rem; color:#94A3B8;">{din.get('desc', 'Lean recovery dinner')}</span>
                            </div>""",
                            unsafe_allow_html=True
                        )

                    with m_col2:
                        lun = day_data.get("lunch", {})
                        st.markdown(
                            f"""<div class="fv-card" style="border-left: 4px solid #F59E0B;">
                                <strong style="color:#FBBF24;">☀️ Lunch ({lun.get('calories', 0)} kcal | {lun.get('protein_g', 0)}g P)</strong><br>
                                <div style="font-weight:700; margin:4px 0;">{lun.get('name', 'Sustained Energy Lunch')}</div>
                                <span style="font-size:0.88rem; color:#94A3B8;">{lun.get('desc', 'Clean macronutrient fuel')}</span>
                            </div>""",
                            unsafe_allow_html=True
                        )

                        snk = day_data.get("snack", {})
                        st.markdown(
                            f"""<div class="fv-card" style="border-left: 4px solid #C084FC;">
                                <strong style="color:#E879F9;">🍎 Metabolic Snack ({snk.get('calories', 0)} kcal | {snk.get('protein_g', 0)}g P)</strong><br>
                                <div style="font-weight:700; margin:4px 0;">{snk.get('name', 'Healthy Snack')}</div>
                                <span style="font-size:0.88rem; color:#94A3B8;">{snk.get('desc', 'Appetite regulating snack')}</span>
                            </div>""",
                            unsafe_allow_html=True
                        )

        # Grocery Shopping List Section
        st.markdown("---")
        st.subheader("🛒 Automated Consolidated Grocery Shopping List")
        st.caption("Consolidated ingredients grouped by supermarket aisle to cover all 7 days of meals.")

        grocery = res.get("consolidated_grocery_list", {})
        g_cols = st.columns(len(grocery) if grocery else 1)

        text_shopping_list = "FOOD VERSE AI - 7-DAY CONSOLIDATED GROCERY LIST\n"
        text_shopping_list += "=" * 50 + "\n\n"

        for i, (aisle, items) in enumerate(grocery.items()):
            text_shopping_list += f"[{aisle.upper()}]\n"
            with g_cols[i % len(g_cols)]:
                st.markdown(f"##### 📦 {aisle}")
                for itm in items:
                    st.markdown(f"- [ ] {itm}")
                    text_shopping_list += f"  - {itm}\n"
            text_shopping_list += "\n"

        # Download Buttons
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.download_button(
                "📋 Download Printable Shopping List (TXT)",
                data=text_shopping_list,
                file_name="foodverse_7day_grocery_shopping_list.txt",
                mime="text/plain",
                use_container_width=True
            )
        with d_col2:
            st.download_button(
                "📥 Export Full 7-Day Plan (JSON)",
                data=json.dumps(res, indent=2),
                file_name="foodverse_7day_metabolic_plan.json",
                mime="application/json",
                use_container_width=True
            )
