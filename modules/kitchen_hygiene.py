"""
Tab 3: Kitchen Hygiene & Food Safety Compliance (Epic 4).
Audits commercial kitchen environments for PPE, hairnets, glove usage,
cross-contamination hazards, sanitization states, and HACCP compliance scores.
"""

import streamlit as st
from PIL import Image
import json
from modules.sample_data import create_sample_kitchen_image
from modules.ui_components import render_compliance_bar_chart, render_provider_badge

def render_kitchen_hygiene_tab(ai_engine):
    st.markdown("### 🧑‍🍳 Commercial Kitchen Hygiene & Food Safety Compliance")
    st.caption("Epic 4 • Computer Vision Inspection for HACCP Compliance, Cross-Contamination Detection, and Sanitation Audits")

    col_input, col_display = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown("#### 1. Kitchen Scene Input")
        source_mode = st.radio(
            "Media Source",
            ["Upload Kitchen Photo / Frame", "Select Standard Audit Test Scene"],
            horizontal=True,
            key="kitchen_source_mode"
        )

        kitchen_type = st.selectbox(
            "Facility Type",
            ["Commercial Restaurant Hot Line", "Cold Prep & Salad Station", "Butchery & Meat Cutting Bay", "Bakery & Pastry Station", "Institutional / Hospital Kitchen"],
            key="kitchen_facility_type"
        )

        selected_image = None

        if source_mode == "Upload Kitchen Photo / Frame":
            uploaded_file = st.file_uploader(
                "Upload kitchen photo (JPEG, PNG, WEBP)",
                type=["jpg", "jpeg", "png", "webp"],
                key="kitchen_uploader"
            )
            if uploaded_file:
                selected_image = Image.open(uploaded_file)
        else:
            sample_choice = st.selectbox(
                "Audit Test Scenarios",
                [
                    "Compliant 5-Star Commercial Station (HACCP Certified)",
                    "Critical Hazard Facility (Raw Poultry Proximity & PPE Violations)"
                ],
                key="sample_kitchen_choice"
            )
            if "Compliant" in sample_choice:
                selected_image = create_sample_kitchen_image("compliant")
            else:
                selected_image = create_sample_kitchen_image("hazard")

        audit_btn = st.button("🛡️ Execute HACCP Safety Compliance Audit", type="primary", use_container_width=True)

    with col_display:
        st.markdown("#### 2. Visual Surveillance Feed")
        if selected_image:
            st.image(selected_image, caption="Surveillance / Audit Frame", use_container_width=True)
        else:
            st.info("👆 Upload an image of a food preparation line or select a test scenario.")

    # Execution
    if audit_btn and selected_image:
        with st.spinner("🔍 Scanning prep stations for PPE compliance, cross-contamination vectors, and chemical storage violations..."):
            audit_result = ai_engine.audit_kitchen_hygiene(selected_image, kitchen_type)
            st.session_state["kitchen_audit_result"] = audit_result

    # Display Results
    if "kitchen_audit_result" in st.session_state and st.session_state["kitchen_audit_result"]:
        res = st.session_state["kitchen_audit_result"]
        st.markdown("---")
        render_provider_badge(res.get("_provider", "demo"), res.get("_model", ""))

        score = res.get("compliance_score_pct", 80)
        grade = res.get("haccp_grade", "Grade B")

        if score >= 85:
            score_color = "#10B981" # Green
            verdict_badge = "badge-success"
        elif score >= 70:
            score_color = "#F59E0B" # Amber
            verdict_badge = "badge-warning"
        else:
            score_color = "#EF4444" # Red
            verdict_badge = "badge-danger"

        # Header Scores
        h1, h2, h3 = st.columns([2.5, 1.2, 1.3])
        with h1:
            st.subheader(f"📋 Inspection: {res.get('kitchen_type', 'Kitchen Facility')}")
            st.markdown(f"**Official HACCP Status:** <span class='badge {verdict_badge}'>{grade}</span>", unsafe_allow_html=True)

        with h2:
            st.metric(label="Compliance Score", value=f"{score}%", delta="HACCP Target ≥85%")

        with h3:
            violations_count = len(res.get("violation_logs", []))
            st.metric(label="Flagged Violations", value=str(violations_count), delta="- Action Required" if violations_count > 0 else "Clear")

        st.info(f"📝 **Executive Summary:** {res.get('executive_summary', 'Inspection complete.')}")

        # Dimension Breakdown & Chart
        d_col1, d_col2 = st.columns([1, 1], gap="medium")

        with d_col1:
            st.markdown("##### 📊 Dimension Compliance Analysis")
            dim_scores = res.get("dimension_scores", {})
            if dim_scores:
                bar_fig = render_compliance_bar_chart(dim_scores)
                st.plotly_chart(bar_fig, use_container_width=True)

        with d_col2:
            st.markdown("##### 📌 Key Compliance Checklist")
            st.markdown(
                f"""<div class="fv-card">
                    <ul style="padding-left:18px; margin:0;">
                        <li><strong>Hair Restraints & Caps:</strong> Mandatory for all prep line personnel.</li>
                        <li><strong>Single-Use Nitrile Gloves:</strong> Required for direct contact with ready-to-eat foods.</li>
                        <li><strong>Cutting Board Protocol:</strong> Strict color coding (Red: Raw Meat, Green: Salad/Veggies, Yellow: Cooked Poultry).</li>
                        <li><strong>Sanitizer Solution:</strong> Verified 200ppm quat or 50-100ppm chlorine bucket test.</li>
                        <li><strong>Chemical Isolation:</strong> All toxic cleaning chemicals stored strictly below food prep height.</li>
                    </ul>
                </div>""",
                unsafe_allow_html=True
            )

        # Itemized Violation Logs
        st.markdown("#### 🚨 Itemized Violation Log & Corrective Actions")
        logs = res.get("violation_logs", [])
        if logs:
            for i, v in enumerate(logs):
                sev = v.get("severity", "MINOR").upper()
                sev_border = "#EF4444" if sev == "CRITICAL" else ("#F59E0B" if sev == "MAJOR" else "#0EA5E9")
                sev_badge = "badge-danger" if sev == "CRITICAL" else ("badge-warning" if sev == "MAJOR" else "badge-info")

                st.markdown(
                    f"""<div class="fv-card" style="border-left: 5px solid {sev_border}; margin-bottom: 12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span class="badge {sev_badge}">{sev} VIOLATION</span>
                            <span style="font-weight:700; color:#94A3B8; font-size:0.85rem;">Category: {v.get('category', 'Hygiene')}</span>
                        </div>
                        <div style="font-size:0.98rem; font-weight:600; color:#F8FAFC; margin-bottom:4px;">
                            ⚠️ Issue: {v.get('issue', 'Non-compliant state')}
                        </div>
                        <div style="font-size:0.9rem; color:#34D399; margin-top:6px; background:rgba(16,185,129,0.08); padding:8px 12px; border-radius:6px;">
                            <strong>🔧 Mandatory Corrective Action:</strong> {v.get('corrective_action', 'Remediate immediately')}
                        </div>
                    </div>""",
                    unsafe_allow_html=True
                )
        else:
            st.success("🎉 Zero safety violations detected! Facility is fully HACCP compliant.")

        st.caption(f"🛡️ {res.get('inspector_signoff', 'Certified HACCP Food Safety Audit System')}")

        with st.expander("📄 Export Kitchen Safety Audit (JSON)"):
            st.json(res)
            st.download_button(
                "📥 Download HACCP Compliance Report",
                data=json.dumps(res, indent=2),
                file_name="kitchen_haccp_audit_report.json",
                mime="application/json"
            )
