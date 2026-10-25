"""
Tab 2: Food Freshness & Spoilage Diagnostic (Epic 3).
Evaluates surface texture, discoloration, wrinkling, mold, freshness classification,
actionable food safety verdicts, and scientific preservation storage tips.
"""

import streamlit as st
from PIL import Image
import json
from modules.sample_data import create_sample_produce_image
from modules.ui_components import render_provider_badge

def render_freshness_tab(ai_engine):
    st.markdown("### 🔬 Food Freshness & Spoilage Diagnostic")
    st.caption("Epic 3 • Computer Vision Surface Texture, Microbial Spoilage, and HACCP Food Safety Assessment")

    col_input, col_display = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown("#### 1. Perishable Item Input")
        source_mode = st.radio(
            "Item Source",
            ["Upload Perishable Item Photo", "Select High-Fidelity Diagnostic Preset"],
            horizontal=True,
            key="freshness_source_mode"
        )

        selected_image = None
        item_category = st.selectbox(
            "Food Category",
            ["Fresh Fruit / Berries", "Leafy Vegetables & Crucifers", "Raw Poultry & Red Meat", "Dairy & Soft Cheeses", "Bakery & Breads"],
            key="freshness_category"
        )

        if source_mode == "Upload Perishable Item Photo":
            uploaded_file = st.file_uploader(
                "Upload photo (JPEG, PNG, WEBP)",
                type=["jpg", "jpeg", "png", "webp"],
                key="freshness_uploader"
            )
            if uploaded_file:
                selected_image = Image.open(uploaded_file)
        else:
            sample_choice = st.selectbox(
                "Diagnostic Preset Scenarios",
                [
                    "Fresh Crisp Honeycrisp Apple (Optimal Turgor)",
                    "Overripe Banana (High Senescence & Browning)",
                    "Spoiled Strawberries (Active Botrytis Mold Colonies)"
                ],
                key="sample_freshness_choice"
            )
            if "Apple" in sample_choice:
                selected_image = create_sample_produce_image("fresh_apple")
            elif "Banana" in sample_choice:
                selected_image = create_sample_produce_image("overripe_banana")
            else:
                selected_image = create_sample_produce_image("spoiled_berries")

        diagnose_btn = st.button("🧪 Run Spoilage & Microbial Diagnostic", type="primary", use_container_width=True)

    with col_display:
        st.markdown("#### 2. Specimen Visual")
        if selected_image:
            st.image(selected_image, caption="Perishable Specimen", use_container_width=True)
        else:
            st.info("👆 Upload an image of produce or raw food, or select a preset to begin.")

    # Run Analysis
    if diagnose_btn and selected_image:
        with st.spinner("🔬 Performing deep visual surface analysis, microbial colony detection, and moisture loss audit..."):
            diag_result = ai_engine.diagnose_freshness(selected_image, item_category)
            st.session_state["freshness_audit_result"] = diag_result

    # Display Results
    if "freshness_audit_result" in st.session_state and st.session_state["freshness_audit_result"]:
        res = st.session_state["freshness_audit_result"]
        st.markdown("---")
        render_provider_badge(res.get("_provider", "demo"), res.get("_model", ""))

        # Top Diagnostic Banner
        stage = res.get("freshness_stage", "Fresh").title()
        verdict = res.get("actionable_safety_verdict", "Safe to consume")
        score = res.get("freshness_score_pct", 85)

        # Color coding for stage
        if "fresh" in stage.lower() and "mod" not in stage.lower():
            stage_color = "#10B981" # Green
            badge_class = "badge-success"
        elif "mod" in stage.lower() or "approach" in stage.lower():
            stage_color = "#F59E0B" # Amber
            badge_class = "badge-warning"
        else:
            stage_color = "#EF4444" # Red
            badge_class = "badge-danger"

        banner_col1, banner_col2, banner_col3 = st.columns([2.5, 1.2, 1.3])
        with banner_col1:
            st.subheader(f"🔍 Specimen: {res.get('item_identified', 'Perishable Item')}")
            st.markdown(f"**Classification:** <span class='badge {badge_class}'>{stage}</span>", unsafe_allow_html=True)

        with banner_col2:
            st.metric(label="Freshness Index", value=f"{score}%", delta="Viability")

        with banner_col3:
            # Actionable Safety Box
            st.markdown(
                f"""<div style="background:rgba(15,23,42,0.8); border:2px solid {stage_color}; border-radius:10px; padding:8px 12px; text-align:center;">
                    <div style="font-size:0.75rem; color:#94A3B8; text-transform:uppercase; font-weight:700;">Actionable Verdict</div>
                    <div style="font-size:1rem; font-weight:800; color:{stage_color}; margin-top:2px;">{verdict}</div>
                </div>""",
                unsafe_allow_html=True
            )

        # Safety Detail Callout
        st.markdown(
            f"""<div class="fv-card" style="border-left: 4px solid {stage_color}; margin-top:14px;">
                <strong>🛡️ Safety & Microbiological Assessment:</strong><br>
                <span>{res.get('actionable_advice_detail', 'No critical hazard detected.')}</span>
            </div>""",
            unsafe_allow_html=True
        )

        # Spoilage Indicators Breakdown
        st.markdown("#### 🔬 Detailed Morphological & Surface Evaluation")
        ind = res.get("spoilage_indicators", {})

        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.markdown(
                f"""<div class="fv-card">
                    <strong style="color:#38BDF8;">1. Surface Texture & Turgidity:</strong><br>
                    <span>{ind.get('surface_texture', 'Intact')}</span>
                </div>""",
                unsafe_allow_html=True
            )
            st.markdown(
                f"""<div class="fv-card">
                    <strong style="color:#FBBF24;">2. Enzymatic Discoloration & Oxidation:</strong><br>
                    <span>{ind.get('discoloration', 'None observed')}</span>
                </div>""",
                unsafe_allow_html=True
            )

        with s_col2:
            st.markdown(
                f"""<div class="fv-card">
                    <strong style="color:#C084FC;">3. Wrinkling & Moisture Desiccation:</strong><br>
                    <span>{ind.get('wrinkling_moisture_loss', 'Zero wrinkling')}</span>
                </div>""",
                unsafe_allow_html=True
            )
            st.markdown(
                f"""<div class="fv-card">
                    <strong style="color:#F87171;">4. Mold Colonies & Fungal Mycelium:</strong><br>
                    <span>{ind.get('mold_or_microbial_growth', 'Negative')}</span>
                </div>""",
                unsafe_allow_html=True
            )

        # Preservation & Storage Guide
        st.markdown("#### ❄️ Proper Food Science Preservation & Storage Protocol")
        guide = res.get("preservation_storage_guide", {})
        g1, g2, g3 = st.columns(3)
        with g1:
            st.info(f"🌡️ **Ideal Temp:**\n\n{guide.get('optimal_temperature_c', '1-4°C')}")
        with g2:
            st.info(f"💧 **Humidity:**\n\n{guide.get('optimal_humidity', '85-90%')}")
        with g3:
            st.info(f"🧊 **Freezing Viability:**\n\n{guide.get('freezing_viability', '6 months')}")

        st.success(f"🌱 **Ethylene Dynamics:** {guide.get('ethylene_sensitivity', 'Standard handling')}")
        st.caption(f"💡 **Shelf Life Extension Secret:** {guide.get('shelf_life_extension_tip', 'Store in dry airtight container.')}")

        # JSON Export
        with st.expander("📄 Export Freshness Diagnostic Report (JSON)"):
            st.json(res)
            st.download_button(
                "📥 Download Diagnostic Report",
                data=json.dumps(res, indent=2),
                file_name=f"freshness_{res.get('item_identified', 'specimen').lower().replace(' ', '_')}.json",
                mime="application/json"
            )
