"""
AI-Based Heart Attack Risk Prediction using Retinal Eye Images
Full workflow: Dashboard, New Analysis, Results & History, Settings.
"""

import os
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
import time
from datetime import datetime

# Public URL when deployed (e.g. Streamlit Cloud). Set env var PUBLIC_APP_URL to your live link.
# Auto-detect Streamlit Cloud URL if running there
def get_app_url():
    """Get the app URL - public if deployed, local otherwise."""
    # Check if explicitly set
    public_url = os.environ.get("PUBLIC_APP_URL", "").strip() or None
    if public_url:
        return public_url
    
    # Try to auto-detect Streamlit Cloud URL
    # Streamlit Cloud sets STREAMLIT_SERVER_URL or we can check hostname
    streamlit_url = os.environ.get("STREAMLIT_SERVER_URL", "").strip()
    if streamlit_url and "streamlit.app" in streamlit_url:
        return streamlit_url.rstrip("/")
    
    # Check if running on Streamlit Cloud by hostname (if available via request)
    # For now, return local
    return "http://localhost:8501"

APP_URL_PUBLIC = get_app_url() if get_app_url() != "http://localhost:8501" else None
APP_URL_LOCAL = "http://localhost:8501"
APP_URL = APP_URL_PUBLIC or APP_URL_LOCAL
IS_PUBLIC = APP_URL_PUBLIC is not None

# ============== PAGE CONFIG ==============
st.set_page_config(
    page_title="Heart Attack Risk Prediction | Retinal Analysis",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============== SESSION STATE ==============
if "analyses" not in st.session_state:
    st.session_state["analyses"] = []
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"
if "risk_score" not in st.session_state:
    st.session_state["risk_score"] = None
if "analysis_done" not in st.session_state:
    st.session_state["analysis_done"] = False

# ============== ENHANCED UI THEME ==============
st.markdown(
    """
    <style>
    /* Premium medical UI - deep navy, coral accent, soft backgrounds */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* Main app background - soft gradient */
    .main { background: linear-gradient(165deg, #f8fafc 0%, #f1f5f9 35%, #e2e8f0 100%); }
    .stApp { background: linear-gradient(165deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%); }
    
    /* Headings - deep navy */
    h1, h2, h3 { color: #0f172a !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
    
    /* Primary buttons - coral to rose */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
        color: white !important; font-weight: 600 !important; border: none !important;
        border-radius: 12px !important; padding: 0.75rem 1.75rem !important;
        transition: all 0.25s ease !important; box-shadow: 0 4px 14px rgba(225, 29, 72, 0.35) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(225, 29, 72, 0.45) !important;
    }
    
    /* Secondary buttons */
    .stButton > button:not([kind="primary"]) {
        background: white !important; color: #0f3460 !important; font-weight: 600 !important;
        border: 2px solid #0f3460 !important; border-radius: 12px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:not([kind="primary"]):hover {
        background: #0f3460 !important; color: white !important; transform: translateY(-2px) !important;
    }
    
    /* Sidebar - dark premium, all text white */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #334155 100%) !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.12);
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] small, [data-testid="stSidebar"] a { color: #ffffff !important; }
    [data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] [data-testid="stCaption"] { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #ffffff !important; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label { color: #ffffff !important; }
    [data-testid="stSidebar"] .stRadio > div { background: rgba(255,255,255,0.06); border-radius: 12px; padding: 8px; }
    [data-testid="stSidebar"] [class*="stMarkdown"] { color: #ffffff !important; }
    [data-testid="stSidebar"] [class*="stMarkdown"] * { color: #ffffff !important; }
    [data-testid="stSidebar"] [class*="stMarkdown"] small { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] label[data-testid="stWidgetLabel"] { color: #ffffff !important; }
    
    /* File uploader - dashed border, soft fill */
    [data-testid="stFileUploader"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%) !important;
        border-radius: 16px !important; padding: 1.75rem !important;
        border: 2px dashed #0ea5e9 !important; box-shadow: 0 4px 20px rgba(15, 52, 96, 0.08);
    }
    
    /* Metric cards - glass style */
    [data-testid="stMetricValue"] { font-weight: 800 !important; letter-spacing: -0.02em !important; }
    
    /* Expander */
    .streamlit-expanderHeader { background: rgba(15, 52, 96, 0.06) !important; border-radius: 12px !important; }
    
    /* Risk badges */
    .badge-low { display: inline-block; background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
    .badge-moderate { display: inline-block; background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
    .badge-high { display: inline-block; background: linear-gradient(135deg, #b91c1c 0%, #dc2626 100%); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
    
    /* Custom card for hero */
    .hero-card {
        background: linear-gradient(135deg, #0f3460 0%, #1e3a5f 50%, #16213e 100%);
        border-radius: 20px; padding: 2rem; color: white; margin-bottom: 1.5rem;
        box-shadow: 0 20px 40px rgba(15, 52, 96, 0.25);
    }
    .hero-card h2 { color: white !important; margin: 0 !important; }
    
    /* Info/Success boxes */
    [data-testid="stAlert"] { border-radius: 12px !important; border-left: 4px solid !important; }
    
    /* Dataframe */
    [data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important; }
    
    /* Footer */
    .app-footer { text-align: center; padding: 1.5rem; color: #64748b; font-size: 0.85rem; margin-top: 3rem; border-top: 1px solid #e2e8f0; }
    
    /* Heart Collaborative branding */
    .heart-collab {
        display: flex; align-items: center; justify-content: center; gap: 0.75rem;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #16213e 100%);
        border-radius: 16px; padding: 1rem 1.5rem; margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 8px 24px rgba(15, 52, 96, 0.3);
    }
    .heart-collab .heart-icon { font-size: 2rem; filter: drop-shadow(0 0 8px rgba(225, 29, 72, 0.5)); }
    .heart-collab .brand { color: #ffffff !important; font-weight: 700; font-size: 1.1rem; letter-spacing: 0.02em; }
    .heart-collab .tagline { color: #e2e8f0 !important; font-size: 0.8rem; margin-left: 0.5rem; }
    /* Application link box in sidebar: white text on dark */
    [data-testid="stSidebar"] .app-link-box { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.2) !important; color: #ffffff !important; }
    [data-testid="stSidebar"] .app-link-box a, [data-testid="stSidebar"] .app-link-box strong, [data-testid="stSidebar"] .app-link-box small { color: #a5f3fc !important; }
    .app-link-box { background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border: 2px solid #059669; border-radius: 12px; padding: 1rem 1.25rem; margin: 0.5rem 0; }
    .app-link-box a { color: #047857; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============== HELPERS ==============
def get_risk_category(score: float) -> tuple:
    """Return (category_name, needle_color)."""
    if score < 30:
        return "Low Risk", "#059669"
    if score < 70:
        return "Moderate Risk", "#d97706"
    return "High Risk", "#b91c1c"

def risk_badge_html(category: str) -> str:
    """Return HTML for risk category badge."""
    c = (category or "").replace(" ", "").lower()
    if "low" in c:
        return '<span class="badge-low">Low Risk</span>'
    if "moderate" in c:
        return '<span class="badge-moderate">Moderate Risk</span>'
    if "high" in c:
        return '<span class="badge-high">High Risk</span>'
    return f'<span class="badge-moderate">{category or "—"}</span>'

def get_recommendation_text(category: str, score: float) -> str:
    """Return short recommendation based on risk category."""
    if category == "Low Risk":
        return "Maintain a healthy lifestyle: regular exercise, balanced diet, and routine check-ups. Retinal screening can be repeated as per your physician's schedule."
    if category == "Moderate Risk":
        return "Consider lifestyle modifications and closer monitoring. Discuss with your doctor: blood pressure, cholesterol, and possible stress tests. Follow-up retinal screening in 6–12 months may be advised."
    return "Prioritize a cardiology consultation. Your doctor may recommend further tests (e.g. ECG, stress test, lipid panel). Adopt heart-healthy habits and adhere to any prescribed treatment. Retinal follow-up as advised."

def get_dummy_risk_score() -> float:
    """Placeholder: random risk 0–100. Replace with real ML model later."""
    return round(random.uniform(0, 100), 1)

def build_gauge_figure(risk_score: float, title: str = "Heart Attack Risk Score"):
    """Build Plotly gauge chart for given score."""
    category, needle_color = get_risk_category(risk_score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            number={"suffix": "%", "font": {"size": 40}},
            title={"text": title, "font": {"size": 22}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": "rgba(0,0,0,0)"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#1a5f7a",
                "steps": [
                    {"range": [0, 30], "color": "rgba(5, 150, 105, 0.65)"},
                    {"range": [30, 70], "color": "rgba(217, 119, 6, 0.65)"},
                    {"range": [70, 100], "color": "rgba(185, 28, 28, 0.65)"},
                ],
                "threshold": {
                    "line": {"color": needle_color, "width": 4},
                    "thickness": 0.8,
                    "value": risk_score,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Plus Jakarta Sans, sans-serif", "color": "#0f172a"},
        margin=dict(l=40, r=40, t=60, b=40),
        height=380,
    )
    return fig

# ============== SIDEBAR: Navigation + Patient Info (contextual) ==============
with st.sidebar:
    # Heart Collaborative branding (medical theme)
    st.markdown(
        '<div class="heart-collab">'
        '<span class="heart-icon">❤️</span>'
        '<span><span class="brand">Heart Collaborative</span><span class="tagline">Medical AI</span></span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    nav_options = ["Dashboard", "New Analysis", "Results & History", "Deploy", "Settings"]
    current_idx = nav_options.index(st.session_state["current_page"]) if st.session_state["current_page"] in nav_options else 0
    page = st.radio(
        "**Navigation**",
        options=nav_options,
        index=current_idx,
        key="nav_radio",
        label_visibility="collapsed",
    )
    st.session_state["current_page"] = page
    st.markdown("---")

    # Patient info only on New Analysis
    if page == "New Analysis":
        st.markdown("### 🏥 Patient Information")
        patient_name = st.text_input("**Patient Name**", placeholder="Enter full name", key="patient_name")
        age = st.number_input("**Age**", min_value=1, max_value=120, value=45, step=1, key="age")
        gender = st.selectbox(
            "**Gender**",
            options=["Male", "Female", "Other", "Prefer not to say"],
            index=0,
            key="gender",
        )
    st.markdown("---")
    # Quick stat
    num_analyses = len(st.session_state.get("analyses", []))
    st.caption(f"📋 {num_analyses} analysis/analyses in this session")
    st.markdown("---")
    # Application link (visible on all pages) - public when deployed, local otherwise
    st.markdown("**🔗 Application link**")
    st.markdown(f"[**Open: {APP_URL}**]({APP_URL})")
    if APP_URL_PUBLIC:
        st.caption("✅ Public link — open for everyone on any device")
        st.caption(f"Share this link: {APP_URL}")
    else:
        st.caption("Local: streamlit run app.py")
        st.caption("Deploy to get: https://heart-project-xxxx.streamlit.app")
    st.markdown("---")
    st.markdown("*Complete the form and run analysis on the main page.*")

# ============== MAIN: Route by page ==============
if page == "Dashboard":
    # Dashboard: white font on dark background (medical theme)
    st.markdown(
        """
        <style>
        .main .block-container { background: linear-gradient(180deg, #0f172a 0%, #1e293b 40%, #334155 100%) !important; padding: 2rem !important; border-radius: 20px !important; color: #ffffff !important; }
        .main .block-container *, .main .block-container p, .main .block-container span, .main .block-container label { color: #f1f5f9 !important; }
        .main .block-container h1, .main .block-container h2, .main .block-container h3 { color: #ffffff !important; }
        .main .block-container [data-testid="stMetricLabel"] { color: #cbd5e1 !important; }
        .main .block-container [data-testid="stMetricValue"] { color: #ffffff !important; }
        .main .block-container [data-testid="stMetricDelta"] { color: #94a3b8 !important; }
        .main .block-container .stCaption { color: #94a3b8 !important; }
        .main .block-container [data-testid="stAlert"] { color: #e2e8f0 !important; }
        .main .block-container [data-testid="stAlert"] * { color: inherit !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    analyses = st.session_state["analyses"]
    n = len(analyses)
    low = sum(1 for a in analyses if a.get("risk_category") == "Low Risk")
    mod = sum(1 for a in analyses if a.get("risk_category") == "Moderate Risk")
    high = sum(1 for a in analyses if a.get("risk_category") == "High Risk")

    # Hero section
    st.markdown(
        f'<div class="hero-card">'
        f'<h2>📊 Heart Risk Analytics</h2>'
        f'<p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Overview of AI-based retinal risk analyses · {n} total run{n if n != 1 else ""}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # KPI row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Analyses", n, help="Number of analyses in this session")
    with col2:
        st.metric("Low Risk", low, help="0–30% risk score")
    with col3:
        st.metric("Moderate", mod, help="30–70% risk score")
    with col4:
        st.metric("High Risk", high, help="70–100% risk score")
    with col5:
        if n > 0:
            avg_risk = sum(a.get("risk_score", 0) for a in analyses) / n
            st.metric("Avg. Score", f"{avg_risk:.1f}%", help="Average risk score")
        else:
            st.metric("Avg. Score", "—", help="Run analyses to see average")

    st.markdown("---")
    row1, row2 = st.columns([1, 1])

    with row1:
        st.markdown("### 📈 Risk Distribution")
        if analyses:
            df_dist = pd.DataFrame({
                "Category": ["Low Risk", "Moderate Risk", "High Risk"],
                "Count": [low, mod, high],
            })
            fig_pie = px.pie(
                df_dist, values="Count", names="Category", color="Category",
                color_discrete_map={"Low Risk": "#059669", "Moderate Risk": "#d97706", "High Risk": "#b91c1c"},
                hole=0.55,
            )
            fig_pie.update_layout(
                showlegend=True, margin=dict(t=20, b=20), height=320,
                paper_bgcolor="rgba(0,0,0,0)", font={"color": "#f1f5f9", "family": "Plus Jakarta Sans"},
                legend={"font": {"color": "#f1f5f9"}},
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No analyses yet. Run an analysis from **New Analysis** to see distribution.")

    with row2:
        st.markdown("### 📉 Risk Trend (last 20)")
        if analyses:
            recent = list(reversed(analyses))[:20]
            df_trend = pd.DataFrame([
                {"#": i + 1, "Score": a.get("risk_score", 0), "Patient": a.get("patient_name", "—")}
                for i, a in enumerate(recent)
            ])
            fig_trend = px.line(df_trend, x="#", y="Score", markers=True, title="")
            fig_trend.update_layout(
                yaxis_range=[0, 100], yaxis_title="Risk %",
                margin=dict(t=10, b=30), height=320,
                paper_bgcolor="rgba(0,0,0,0)", font={"color": "#f1f5f9"},
                plot_bgcolor="rgba(255,255,255,0.12)", xaxis={"gridcolor": "rgba(255,255,255,0.2)"}, yaxis={"gridcolor": "rgba(255,255,255,0.2)"},
            )
            fig_trend.add_hrect(y0=0, y1=30, line_width=0, fillcolor="green", opacity=0.08)
            fig_trend.add_hrect(y0=30, y1=70, line_width=0, fillcolor="orange", opacity=0.08)
            fig_trend.add_hrect(y0=70, y1=100, line_width=0, fillcolor="red", opacity=0.08)
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("Run analyses to see risk trend over time.")

    st.markdown("---")
    wcol1, wcol2 = st.columns([1, 1])
    with wcol2:
        st.markdown("### 🧭 Workflow")
        st.markdown("""
        1. **New Analysis** → Enter patient details and optional clinical parameters.
        2. **Upload** → Add a retinal fundus image (JPG/PNG).
        3. **Run** → Click *RUN V5.2 ANALYSIS* and wait for the result.
        4. **Review** → See gauge, category, and recommendations; result is saved.
        5. **Results & History** → View, filter, or export all past analyses.
        """)
        if st.button("➡️ Go to New Analysis", use_container_width=True):
            st.session_state["current_page"] = "New Analysis"
            st.rerun()

    with wcol1:
        st.markdown("### 🕐 Recent Activity")
        if analyses:
            recent = list(reversed(analyses))[:10]
            for a in recent:
                cat = a.get("risk_category", "—")
                name = a.get("patient_name") or "—"
                ts = a.get("timestamp", "—")
                score = a.get("risk_score", "—")
                badge = risk_badge_html(cat)
                st.markdown(f"**{name}** {badge} **{score}%** · *{ts}*", unsafe_allow_html=True)
        else:
            st.caption("No analyses recorded yet.")
    st.markdown("---")
    st.markdown(
        f'❤️ Heart Collaborative · [**Open app: {APP_URL}**]({APP_URL}) · Demo · Not medical advice · v1.0'
    )

# ---------------------------------------------------------------------------
elif page == "New Analysis":
    st.markdown(
        '<div class="hero-card" style="padding: 1.25rem 2rem;">'
        '<h2 style="margin:0;">❤️ New Analysis</h2>'
        '<p style="margin: 0.4rem 0 0 0; opacity: 0.9;">Retinal fundus image analysis for cardiovascular risk assessment</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Clinical options (expandable)
    with st.expander("📋 Clinical Parameters (optional)", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            bp_sys = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=200, value=120, key="bp_sys")
            cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=200, key="chol")
        with c2:
            bp_dia = st.number_input("Diastolic BP (mmHg)", min_value=50, max_value=130, value=80, key="bp_dia")
            bmi = st.number_input("BMI", min_value=15.0, max_value=50.0, value=24.0, step=0.1, key="bmi")
        with c3:
            smoking = st.selectbox("Smoking", ["No", "Yes"], key="smoking")
            diabetes = st.selectbox("Diabetes", ["No", "Yes"], key="diabetes")

    col_upload, col_info = st.columns([2, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "**Upload Retinal Fundus Image**",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=False,
            help="Drag and drop your retinal (fundus) image here.",
            key="retinal_upload",
        )
    with col_info:
        patient_name = st.session_state.get("patient_name") or ""
        age = st.session_state.get("age", 45)
        gender = st.session_state.get("gender", "Male")
        if patient_name:
            st.info(f"**Patient:** {patient_name}  \n**Age:** {age}  \n**Gender:** {gender}")
        if uploaded_file:
            st.success(f"✅ **{uploaded_file.name}** uploaded")

    st.markdown("---")
    run_analysis = st.button("🔬 RUN V5.2 ANALYSIS", type="primary", use_container_width=True)

    if run_analysis:
        progress_bar = st.progress(0)
        status_text = st.empty()
        with st.spinner("Analyzing retinal image and computing risk score..."):
            for i in range(1, 101):
                time.sleep(0.02)
                progress_bar.progress(i)
                status_text.text(f"Analysis in progress... {i}%")
            risk_score = get_dummy_risk_score()
            status_text.text("Analysis complete!")
        progress_bar.empty()
        status_text.empty()

        category, _ = get_risk_category(risk_score)
        st.session_state["risk_score"] = risk_score
        st.session_state["analysis_done"] = True

        # Append to history
        record = {
            "patient_name": patient_name or "Unknown",
            "age": age,
            "gender": gender,
            "risk_score": risk_score,
            "risk_category": category,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "bp_sys": bp_sys,
            "bp_dia": bp_dia,
            "cholesterol": cholesterol,
            "smoking": smoking,
            "diabetes": diabetes,
            "bmi": bmi,
            "image_name": uploaded_file.name if uploaded_file else None,
        }
        st.session_state["analyses"] = st.session_state["analyses"] + [record]
        st.success(f"Result saved. Risk: **{category}** ({risk_score}%). View in **Results & History** or below.")

    # Show gauge after analysis (current or from last run on this page)
    if st.session_state.get("analysis_done") and st.session_state.get("risk_score") is not None:
        risk_score = st.session_state["risk_score"]
        category, _ = get_risk_category(risk_score)
        st.markdown("### 📊 Risk Assessment Result")
        st.plotly_chart(build_gauge_figure(risk_score), use_container_width=True)
        st.markdown(f"**Risk Category:** {risk_badge_html(category)}", unsafe_allow_html=True)
        st.markdown("---")
        with st.expander("💡 Recommendations", expanded=True):
            st.markdown(get_recommendation_text(category, risk_score))
        with st.expander("📄 Report summary (copy for records)"):
            pname = st.session_state.get("patient_name") or "—"
            page_val = st.session_state.get("age", "—")
            pgender = st.session_state.get("gender", "—")
            report = f"""
**Heart Attack Risk Assessment — Retinal Analysis**
Patient: {pname} | Age: {page_val} | Gender: {pgender}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Risk Score: {risk_score}% | Category: {category}

Clinical (if provided): BP {st.session_state.get('bp_sys', '—')}/{st.session_state.get('bp_dia', '—')} mmHg, Cholesterol {st.session_state.get('cholesterol', '—')} mg/dL, BMI {st.session_state.get('bmi', '—')}, Smoking: {st.session_state.get('smoking', '—')}, Diabetes: {st.session_state.get('diabetes', '—')}

Recommendation: {get_recommendation_text(category, risk_score)}

— Generated by Heart Risk AI (demo). Not a substitute for professional medical advice.
            """.strip()
            st.text_area("Copy report", value=report, height=220, key="report_text", label_visibility="collapsed")
        st.caption("Green = Low (0–30%) | Amber = Moderate (30–70%) | Red = High (70–100%). Dummy model.")
    else:
        st.info("👆 Upload a retinal image and click **RUN V5.2 ANALYSIS** to see the risk gauge.")
    st.markdown("---")
    st.markdown(
        f'❤️ Heart Collaborative · [**Open app: {APP_URL}**]({APP_URL}) · Demo · Not medical advice · v1.0'
    )

# ---------------------------------------------------------------------------
elif page == "Results & History":
    st.title("📁 Results & History")
    st.markdown("**View and export all past risk analyses**")
    st.markdown("---")

    analyses = st.session_state["analyses"]
    if not analyses:
        st.info("No analyses yet. Run an analysis from **New Analysis** first.")
    else:
        df = pd.DataFrame(analyses)
        # Columns to show in table
        cols_show = ["timestamp", "patient_name", "age", "gender", "risk_score", "risk_category"]
        cols_show = [c for c in cols_show if c in df.columns]
        df_display = df[cols_show].copy()
        df_display = df_display.rename(columns={
            "timestamp": "Date/Time",
            "patient_name": "Patient",
            "risk_score": "Score %",
            "risk_category": "Category",
        })

        # Filters
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filter_cat = st.selectbox("Filter by category", ["All", "Low Risk", "Moderate Risk", "High Risk"], key="filter_cat")
        with col_f2:
            filter_name = st.text_input("Filter by patient name", placeholder="Name...", key="filter_name")
        with col_f3:
            st.download_button(
                "📥 Export CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"heart_risk_analyses_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        mask = pd.Series([True] * len(df))
        if filter_cat != "All":
            mask &= df["risk_category"] == filter_cat
        if filter_name:
            mask &= df["patient_name"].str.contains(filter_name, case=False, na=False)
        df_filtered = df_display[mask]

        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

        st.markdown("### View detail")
        indices = list(range(len(analyses)))
        labels = [f"{a.get('patient_name', '—')} — {a.get('risk_category', '—')} ({a.get('risk_score', '—')}%)" for a in analyses]
        sel_idx = st.selectbox("Select an analysis to view gauge", range(len(analyses)), format_func=lambda i: labels[i], key="sel_hist")
        if sel_idx is not None and 0 <= sel_idx < len(analyses):
            a = analyses[sel_idx]
            st.plotly_chart(build_gauge_figure(a["risk_score"], f"Risk — {a.get('patient_name', 'Patient')}"), use_container_width=True)
            st.markdown("**Recommendation:** " + get_recommendation_text(a.get("risk_category", ""), a.get("risk_score", 0)))
            with st.expander("Full record (JSON)"):
                st.json({k: v for k, v in a.items() if v is not None})
    st.markdown("---")
    st.markdown(
        f'❤️ Heart Collaborative · [**Open app: {APP_URL}**]({APP_URL}) · Demo · Not medical advice · v1.0'
    )

# ---------------------------------------------------------------------------
elif page == "Deploy":
    st.title("🌐 Deploy — Make App Open for Everyone")
    st.markdown("**Get a public link that anyone can open from any device**")
    st.markdown("---")
    
    st.info("""
    **Goal:** Deploy your app to get a public link like `https://heart-project-xxxx.streamlit.app` 
    that **anyone** can open from **any device** (phone, tablet, laptop) — no installation needed.
    """)
    
    st.markdown("### ✅ Quick Steps (5 minutes)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Create GitHub Repository
        
        1. Go to **[github.com](https://github.com)** and sign up (free).
        2. Click **"New repository"**.
        3. Name it: `Heart-Project`.
        4. Make it **Public**.
        5. Click **"Create repository"**.
        
        #### 2️⃣ Upload Your Code
        
        **Using GitHub Website:**
        - In your repository, click **"uploading an existing file"**.
        - Drag and drop: `app.py`, `requirements.txt`, `README.md`.
        - Click **"Commit changes"**.
        """)
    
    with col2:
        st.markdown("""
        #### 3️⃣ Deploy on Streamlit Cloud
        
        1. Go to **[share.streamlit.io](https://share.streamlit.io)**.
        2. Click **"Sign in"** → Sign in with **GitHub**.
        3. Click **"New app"**.
        4. Choose:
           - **Repository:** `YOUR-USERNAME/Heart-Project`
           - **Branch:** `main`
           - **Main file:** `app.py`
        5. Click **"Deploy!"**.
        
        #### 4️⃣ Get Your Public Link
        
        Wait 2-3 minutes. Your app will be live at:
        
        **`https://heart-project-xxxx.streamlit.app`**
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Checklist")
    
    checklist = st.container()
    with checklist:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.checkbox("GitHub account created")
            st.checkbox("Repository created (public)")
        with col2:
            st.checkbox("Code uploaded (`app.py`, `requirements.txt`)")
            st.checkbox("Signed in to Streamlit Cloud")
        with col3:
            st.checkbox("App deployed")
            st.checkbox("Public link received")
    
    st.markdown("---")
    st.markdown("### 🎯 After Deployment")
    
    st.success("""
    ✅ Your app is **live 24/7** (always running).  
    ✅ **Anyone** can open it from any device (phone, tablet, laptop).  
    ✅ **No installation** needed for users.  
    ✅ **Free** hosting (Streamlit Community Cloud).  
    ✅ **Automatic updates** — when you push code to GitHub, the app updates automatically.
    """)
    
    st.markdown("### 🔗 Share Your Link")
    st.markdown("""
    Once deployed, share your link (`https://heart-project-xxxx.streamlit.app`) via:
    - Email
    - WhatsApp / Telegram
    - Social media
    - Website
    - QR code
    
    **Anyone who clicks it can use your app immediately!**
    """)
    
    st.markdown("---")
    st.markdown("### 📚 Detailed Guide")
    st.markdown("""
    For step-by-step instructions with screenshots, see:
    - **[DEPLOY_SIMPLE.md](DEPLOY_SIMPLE.md)** — Simple, beginner-friendly guide
    - **[DEPLOY.md](DEPLOY.md)** — Detailed deployment guide
    """)
    
    st.markdown("---")
    st.markdown(
        f'❤️ Heart Collaborative · [**Open app: {APP_URL}**]({APP_URL}) · Demo · Not medical advice · v1.0'
    )

# ---------------------------------------------------------------------------
elif page == "Settings":
    st.title("⚙️ Settings")
    st.markdown("**Application and model configuration**")
    st.markdown("---")
    st.selectbox("Model version", ["V5.2 (current)", "V5.1", "V5.0"], key="model_ver")
    st.markdown("---")
    if st.button("🗑️ Clear all analysis history (session only)", type="secondary"):
        st.session_state["analyses"] = []
        st.session_state["risk_score"] = None
        st.session_state["analysis_done"] = False
        st.rerun()
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    **AI-Based Heart Attack Risk Prediction** uses retinal fundus images to estimate cardiovascular risk.
    - This is a **demo** with dummy predictions. Replace the model in code for real inference.
    - Always consult a healthcare provider for medical decisions.
    - Data is stored in session only (not persisted to disk).
    """)
    st.caption("Built with Streamlit · Medical theme · Full workflow: Dashboard → New Analysis → Results & History.")
    st.markdown("---")
    st.markdown(
        f'❤️ Heart Collaborative · [**Open app: {APP_URL}**]({APP_URL}) · Demo · Not medical advice · v1.0'
    )

