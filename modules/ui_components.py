"""
UI Components, Custom CSS, and Interactive Charts for Food Verse AI.
"""

import streamlit as st
import plotly.graph_objects as go

def apply_custom_css():
    """Injects modern, vibrant, and production-grade CSS styling into the Streamlit app."""
    css = """
    <style>
    /* Google Fonts & Root Theme */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Gradient Hero Container */
    .hero-container {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(14, 165, 233, 0.08) 50%, rgba(245, 158, 11, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px -4px rgba(0, 0, 0, 0.2);
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #10B981, #06B6D4, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.02rem;
        margin: 0;
        font-weight: 500;
    }

    .capstone-tag {
        display: inline-block;
        background: rgba(16, 185, 129, 0.18);
        color: #34D399;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 3px 10px;
        border-radius: 999px;
        border: 1px solid rgba(52, 211, 153, 0.35);
        margin-bottom: 8px;
    }

    /* Cards */
    .fv-card {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .fv-card:hover {
        border-color: rgba(16, 185, 129, 0.4);
    }

    /* Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 12px;
        margin: 12px 0 18px 0;
    }

    .metric-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 14px 16px;
        text-align: center;
    }

    .metric-val {
        font-size: 1.6rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.2;
    }

    .metric-unit {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94A3B8;
        margin-left: 2px;
    }

    .metric-lbl {
        font-size: 0.78rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-top: 4px;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .badge-success {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .badge-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .badge-danger {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    .badge-info {
        background: rgba(14, 165, 233, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(14, 165, 233, 0.4);
    }

    .badge-model {
        background: rgba(168, 85, 247, 0.15);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.35);
        font-size: 0.75rem;
    }

    /* Health Grade Pill */
    .health-grade-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 64px;
        height: 64px;
        border-radius: 50%;
        font-size: 1.8rem;
        font-weight: 800;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .grade-A { background: linear-gradient(135deg, #059669, #10B981); color: #fff; }
    .grade-B { background: linear-gradient(135deg, #10B981, #84CC16); color: #fff; }
    .grade-C { background: linear-gradient(135deg, #F59E0B, #EAB308); color: #fff; }
    .grade-D { background: linear-gradient(135deg, #EA580C, #F97316); color: #fff; }
    .grade-F { background: linear-gradient(135deg, #DC2626, #EF4444); color: #fff; }

    /* Violation Box */
    .violation-card {
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 4px solid;
    }

    .violation-critical {
        background: rgba(239, 68, 68, 0.12);
        border-color: #EF4444;
    }

    .violation-major {
        background: rgba(245, 158, 11, 0.12);
        border-color: #F59E0B;
    }

    .violation-minor {
        background: rgba(14, 165, 233, 0.12);
        border-color: #0EA5E9;
    }

    /* Recipe Step List */
    .step-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .step-num {
        background: #10B981;
        color: #0F172A;
        font-weight: 800;
        font-size: 0.8rem;
        border-radius: 50%;
        min-width: 24px;
        height: 24px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        flex-shrink: 0;
        margin-top: 2px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_hero_banner():
    """Renders the top application branding banner."""
    html = """
    <div class="hero-container">
        <span class="capstone-tag">Skill Wallet • Capstone Project 3</span>
        <h1 class="hero-title">Food Verse AI</h1>
        <p class="hero-subtitle">
            Multimodal Food Intelligence Agent • Precision Nutrition • Microbial Spoilage Diagnostics • HACCP Hygiene Audit • Culinary Synthesis • Adaptive Metabolic Planning
        </p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_provider_badge(provider: str, model_name: str = ""):
    """Renders a pill showing the active AI engine."""
    prov = (provider or "demo").upper()
    if prov == "GEMINI":
        badge = f'<span class="badge badge-success">🤖 Powered by Google Gemini ({model_name or "gemini-3.8-flash"})</span>'
    elif prov == "GROQ":
        badge = f'<span class="badge badge-info">⚡ Powered by Groq Ultra-Fast AI ({model_name or "llama-3.3-70b"})</span>'
    else:
        badge = '<span class="badge badge-warning">🧪 Interactive Standalone Demonstration Mode (Offline Heuristics)</span>'
    st.markdown(badge, unsafe_allow_html=True)


def render_macro_donut_chart(protein_g: float, carbs_g: float, fats_g: float):
    """Renders an interactive Plotly donut chart representing macronutrient caloric distribution."""
    # Convert grams to kcal: Protein (4), Carbs (4), Fat (9)
    p_kcal = protein_g * 4
    c_kcal = carbs_g * 4
    f_kcal = fats_g * 9
    total_kcal = p_kcal + c_kcal + f_kcal

    if total_kcal <= 0:
        total_kcal = 1

    p_pct = (p_kcal / total_kcal) * 100
    c_pct = (c_kcal / total_kcal) * 100
    f_pct = (f_kcal / total_kcal) * 100

    labels = ['Protein (4 kcal/g)', 'Carbohydrates (4 kcal/g)', 'Fats (9 kcal/g)']
    values = [p_kcal, c_kcal, f_kcal]
    colors = ['#10B981', '#06B6D4', '#F59E0B']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color='#0F172A', width=2)),
        textinfo='percent',
        hoverinfo='label+value',
        textfont=dict(size=13, color='#FFFFFF', family='Plus Jakarta Sans')
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#94A3B8")),
        margin=dict(t=10, b=30, l=10, r=10),
        height=260,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[
            dict(
                text=f"<b>{int(total_kcal)}</b><br><span style='font-size:11px;color:#94A3B8;'>MACRO KCAL</span>",
                x=0.5, y=0.5,
                font=dict(size=18, color='#F8FAFC', family='Space Grotesk'),
                showarrow=False
            )
        ]
    )
    return fig


def render_compliance_bar_chart(dimension_scores: dict):
    """Renders a clean horizontal bar chart of HACCP compliance scores."""
    labels = []
    scores = []
    colors = []

    label_map = {
        "ppe_adherence": "PPE & Hairnet Adherence",
        "cross_contamination_control": "Cross-Contamination Prevention",
        "sanitization_cleanliness": "Sanitization & Stainless Cleanliness",
        "chemical_storage_safety": "Chemical & Allergen Isolation"
    }

    for key, val in dimension_scores.items():
        lbl = label_map.get(key, key.replace("_", " ").title())
        labels.append(lbl)
        scores.append(val)
        if val >= 85:
            colors.append('#10B981')
        elif val >= 70:
            colors.append('#F59E0B')
        else:
            colors.append('#EF4444')

    fig = go.Figure(go.Bar(
        x=scores,
        y=labels,
        orientation='h',
        marker=dict(color=colors, line=dict(color='rgba(255,255,255,0.1)', width=1)),
        text=[f"{s}%" for s in scores],
        textposition='auto',
        textfont=dict(color='#FFFFFF', size=12, family='Plus Jakarta Sans')
    ))

    fig.update_layout(
        xaxis=dict(range=[0, 100], gridcolor='rgba(148, 163, 184, 0.1)', tickfont=dict(color='#94A3B8')),
        yaxis=dict(tickfont=dict(color='#F8FAFC', size=12)),
        margin=dict(t=10, b=20, l=10, r=10),
        height=220,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig
