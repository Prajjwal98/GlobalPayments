import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import time
import random

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Global Payments AI Platform",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. STATE MANAGEMENT & THEME
# ==========================================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

IS_DARK = st.session_state.theme == "dark"

if "step" not in st.session_state:
    st.session_state.step = 1

if "data_enriched" not in st.session_state:
    st.session_state.data_enriched = False

if "data_masked" not in st.session_state:
    st.session_state.data_masked = False

if "model_generated" not in st.session_state:
    st.session_state.model_generated = False

# ==========================================
# 3. CSS DESIGN SYSTEM
# ==========================================
# Using Zinc/shadcn inspired theme
bg = "#09090b" if IS_DARK else "#ffffff"
bg_subtle = "#0c0c0f" if IS_DARK else "#f9fafb"
card = "#0c0c0f" if IS_DARK else "#ffffff"
border = "#1e1e24" if IS_DARK else "#e4e4e7"
border_subtle = "#16161a" if IS_DARK else "#f0f0f2"
text = "#fafafa" if IS_DARK else "#09090b"
text_dim = "#52525b" if IS_DARK else "#a1a1aa"
green = "#22c55e" if IS_DARK else "#16a34a"
green_muted = "rgba(34,197,94,0.12)" if IS_DARK else "rgba(22,163,74,0.08)"
red = "#ef4444" if IS_DARK else "#dc2626"
red_muted = "rgba(239,68,68,0.12)" if IS_DARK else "rgba(220,38,38,0.08)"
shadow = "none" if IS_DARK else "0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03)"

css = f"""
<style>
/* Variables */
:root {{
    --bg: {bg};
    --bg-subtle: {bg_subtle};
    --card: {card};
    --border: {border};
    --border-subtle: {border_subtle};
    --text: {text};
    --text-muted: #71717a;
    --text-dim: {text_dim};
    --accent: #2563eb;
    --green: {green};
    --green-muted: {green_muted};
    --red: {red};
    --red-muted: {red_muted};
    --shadow: {shadow};
    --radius: 10px;
}}

/* Hide Streamlit chrome */
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton {{
    display: none !important;
}}

/* Global styling */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', -apple-system, sans-serif !important;
}}

.block-container {{
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1400px !important;
}}

/* Component styling */
.metric-card {{ background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem 1.4rem; box-shadow: var(--shadow); }}
.metric-label {{ font-size: 0.85rem; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }}
.metric-value {{ font-size: 2rem; font-weight: 700; color: var(--text); letter-spacing: -0.03em; margin-top: 0.3rem; }}
.metric-delta {{ font-size: 0.75rem; font-weight: 500; margin-top: 0.4rem; padding: 2px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 3px; }}
.delta-up {{ color: var(--green); background: var(--green-muted); }}
.delta-down {{ color: var(--red); background: var(--red-muted); }}

.chart-wrap {{ background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.2rem 1.2rem 0.6rem; box-shadow: var(--shadow); }}
.chart-title {{ font-size: 1rem; font-weight: 600; color: var(--text); margin-bottom: 0.2rem; }}
.chart-subtitle {{ font-size: 0.8rem; color: var(--text-dim); margin-bottom: 1rem; }}

.data-table {{ width: 100%; border-collapse: separate; border-spacing: 0; font-size: 0.85rem; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }}
.data-table th {{ text-align: left; padding: 0.8rem 1rem; color: var(--text-muted); font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 1px solid var(--border); background: var(--bg-subtle); }}
.data-table td {{ padding: 0.75rem 1rem; color: var(--text); border-bottom: 1px solid var(--border-subtle); }}
.data-table tr:last-child td {{ border-bottom: none; }}
.data-table td.highlight {{ background-color: rgba(37,99,235,0.05); font-weight: 500; color: var(--accent); }}

.badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }}
.badge-green {{ color: var(--green); background: var(--green-muted); }}
.badge-blue {{ color: var(--accent); background: rgba(37,99,235,0.1); border: 1px solid rgba(37,99,235,0.2); }}

.brand {{ font-size: 1.4rem; font-weight: 800; color: var(--text); letter-spacing: -0.02em; display: flex; align-items: center; gap: 0.5rem; }}
.brand-icon {{ color: var(--accent); }}

.step-card {{ background: var(--bg-subtle); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }}
.step-title {{ font-size: 0.9rem; font-weight: 600; color: var(--text); }}
.step-desc {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem; }}

hr {{ border-color: var(--border) !important; }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ==========================================
# 4. HELPER COMPONENTS
# ==========================================
def metric_card(label, value, delta=None, delta_type="up"):
    cls = f"delta-{delta_type}"
    arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "→")
    delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_table(df, highlight_cols=None):
    highlight_cols = highlight_cols or []
    
    html = '<table class="data-table"><thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    
    for _, row in df.iterrows():
        html += '<tr>'
        for col in df.columns:
            td_class = 'highlight' if col in highlight_cols else ''
            val = row[col]
            html += f'<td class="{td_class}">{val}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    st.markdown(html, unsafe_allow_html=True)

# ==========================================
# 5. MOCK DATA
# ==========================================
@st.cache_data
def get_mock_data():
    raw_txns = pd.DataFrame({
        "txn_id": [f"TXN-{random.randint(1000,9999)}" for _ in range(5)],
        "usr_idx": [f"U-{random.randint(100,999)}" for _ in range(5)],
        "merch_cd": [f"M-{random.randint(10,99)}" for _ in range(5)],
        "amt_val": [round(random.uniform(10, 500), 2) for _ in range(5)],
        "ts_dt": ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05"],
        "cc_num": [f"{random.randint(4000,5000)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}" for _ in range(5)],
        "usr_nm": ["John Doe", "Jane Smith", "Alice Jones", "Bob Brown", "Charlie Day"]
    })
    
    return raw_txns

df_raw = get_mock_data()

# ==========================================
# 6. HEADER & SIDEBAR
# ==========================================
head_left, head_right = st.columns([9, 1])
with head_left:
    st.markdown("""
    <div class="brand">
        <span class="brand-icon">◆</span>
        <span class="brand-name">GlobalPayments Data Fabric POC</span>
    </div>
    """, unsafe_allow_html=True)
with head_right:
    theme_label = "☀️ Light" if IS_DARK else "🌙 Dark"
    st.button(theme_label, on_click=toggle_theme, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 20px;">
        <h2 style="font-size: 1.2rem; font-weight: 700;">Workflow Pipeline</h2>
        <p style="font-size: 0.85rem; color: var(--text-muted);">Demonstrating AI-driven data transformation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    steps = [
        "1. Ingestion & Enrichment",
        "2. Governance & Security",
        "3. Schema Discovery",
        "4. AI Data Modeling",
        "5. Data Product Activation"
    ]
    
    for i, step_name in enumerate(steps, 1):
        if st.button(step_name, use_container_width=True, type="primary" if st.session_state.step == i else "secondary"):
            st.session_state.step = i

# ==========================================
# 7. MAIN VIEWS
# ==========================================
if st.session_state.step == 1:
    st.markdown("### Step 1: Data Ingestion & Enrichment")
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 20px;'>Transforming raw, undocumented operational data into understandable assets using Gemini LLM.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Raw Operational Data** (Before)")
        render_table(df_raw)
        
    with col2:
        st.markdown("**AI Enriched Data** (After)")
        if st.session_state.data_enriched:
            df_enriched = df_raw.copy()
            df_enriched.rename(columns={
                "txn_id": "Transaction ID",
                "usr_idx": "User ID",
                "merch_cd": "Merchant Code",
                "amt_val": "Transaction Amount ($)",
                "ts_dt": "Timestamp",
                "cc_num": "Credit Card",
                "usr_nm": "Customer Name"
            }, inplace=True)
            
            # AI Derived fields
            df_enriched["Customer LTV ($)"] = [round(val * random.uniform(1.5, 3.0), 2) for val in df_enriched["Transaction Amount ($)"]]
            df_enriched["Segment"] = ["High Value", "Mid Value", "Low Value", "High Value", "Mid Value"]
            
            render_table(df_enriched, highlight_cols=["Customer LTV ($)", "Segment"])
            st.success("✨ Metadata descriptions generated & derived fields added via Gemini API.")
        else:
            st.info("Awaiting AI enrichment...")
            if st.button("✨ Suggest Derived Fields & Descriptions", type="primary"):
                with st.spinner("Analyzing schema with Gemini LLM..."):
                    time.sleep(2)
                    st.session_state.data_enriched = True
                    st.rerun()

elif st.session_state.step == 2:
    st.markdown("### Step 2: Governance & Security Scanning")
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 20px;'>Automatically detecting PII via Cloud DLP and applying masking policies.</p>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Total Records Scanned", "45,201")
    with c2: metric_card("PII Entities Found", "3,402", delta="12%", delta_type="up")
    with c3: metric_card("Sensitive Columns", "2", delta="Credit Card, Name", delta_type="warn")
    with c4: metric_card("DLP Confidence", "99.8%")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    mask_toggle = st.toggle("🛡️ Apply AI Masking Policies", value=st.session_state.data_masked)
    st.session_state.data_masked = mask_toggle
    
    df_display = df_raw.copy()
    if st.session_state.data_enriched:
        df_display.rename(columns={
            "txn_id": "Transaction ID", "usr_idx": "User ID", "merch_cd": "Merchant Code", 
            "amt_val": "Amount ($)", "ts_dt": "Timestamp", "cc_num": "Credit Card", "usr_nm": "Customer Name"
        }, inplace=True)
    else:
        # Just to ensure the masking logic finds the right columns even if not enriched
        pass
        
    if st.session_state.data_masked:
        cc_col = "Credit Card" if "Credit Card" in df_display.columns else "cc_num"
        name_col = "Customer Name" if "Customer Name" in df_display.columns else "usr_nm"
        
        df_display[cc_col] = df_display[cc_col].apply(lambda x: f"****-****-****-{x.split('-')[-1]}")
        df_display[name_col] = "[PERSON_NAME]"
    
    st.markdown("**Governance Preview Table**")
    render_table(df_display)

elif st.session_state.step == 3:
    st.markdown("### Step 3: Schema Discovery & Relationship Mapping")
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 20px;'>Using LLMs to analyze query history and automatically infer relationships between data silos.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Inferred Entity Graph</div>
            <div class="chart-subtitle">Nodes represent discovered tables, edges indicate inferred JOINs.</div>
        """, unsafe_allow_html=True)
        
        # Simple NetworkX graph using Plotly
        G = nx.Graph()
        G.add_node("Transactions", type="Core")
        G.add_node("Users", type="Dimension")
        G.add_node("Merchants", type="Dimension")
        G.add_node("GeoLocation", type="Dimension")
        
        G.add_edge("Transactions", "Users", weight=0.95)
        G.add_edge("Transactions", "Merchants", weight=0.88)
        G.add_edge("Users", "GeoLocation", weight=0.75)
        G.add_edge("Merchants", "GeoLocation", weight=0.60)
        
        pos = nx.spring_layout(G, seed=42)
        
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="top center",
            marker=dict(
                color='#2563eb',
                size=30,
                line_width=2
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=20),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("#### AI Join Explainability")
        st.markdown("""
        <div class="step-card">
            <div class="step-title">Transactions ↔ Users</div>
            <div class="step-desc"><strong>95% Confidence</strong>. Historical query logs show these tables are joined on `usr_idx` and `user_id` 95% of the time in the last 30 days.</div>
        </div>
        <div class="step-card">
            <div class="step-title">Transactions ↔ Merchants</div>
            <div class="step-desc"><strong>88% Confidence</strong>. Joined on `merch_cd` in financial reporting queries.</div>
        </div>
        <div class="step-card">
            <div class="step-title">Users ↔ GeoLocation</div>
            <div class="step-desc"><strong>75% Confidence</strong>. Inferred via fuzzy match on `zip_code` and `postal_cd`.</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.step == 4:
    st.markdown("### Step 4: AI Prompt-to-Model Studio")
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 20px;'>Generate the final Data Product using natural language.</p>", unsafe_allow_html=True)
    
    prompt = st.text_area("Describe your target data product:", value="Create a data model to identify high-value users in Europe who frequently purchase electronics, for our next marketing campaign.")
    
    if st.button("Generate Data Model", type="primary"):
        with st.spinner("Synthesizing schemas and writing SQL DDL..."):
            time.sleep(2)
            st.session_state.model_generated = True
            
    if st.session_state.model_generated:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Generated Target Schema**")
            st.markdown("""
            ```json
            {
              "table_name": "marketing_high_value_eu_electronics",
              "schema": [
                {"name": "user_id", "type": "STRING", "description": "Unique user identifier"},
                {"name": "customer_ltv", "type": "FLOAT", "description": "Predicted lifetime value"},
                {"name": "electronics_spend_30d", "type": "FLOAT", "description": "Spend on electronics in 30 days"},
                {"name": "country", "type": "STRING", "description": "European country code"}
              ]
            }
            ```
            """)
        with col2:
            st.markdown("**Generated BigQuery SQL**")
            st.markdown("""
            ```sql
            CREATE OR REPLACE TABLE `global-payments-poc.data_products.marketing_target` AS
            SELECT 
                u.user_id,
                SUM(t.amt_val) * 2.5 AS customer_ltv,
                SUM(CASE WHEN m.category = 'Electronics' THEN t.amt_val ELSE 0 END) AS electronics_spend_30d,
                g.country
            FROM 
                `raw_data.transactions` t
            JOIN `raw_data.users` u ON t.usr_idx = u.user_id
            JOIN `raw_data.merchants` m ON t.merch_cd = m.merchant_code
            JOIN `raw_data.geolocation` g ON u.zip_code = g.postal_code
            WHERE 
                g.region = 'Europe'
            GROUP BY 1, 4
            HAVING electronics_spend_30d > 500;
            ```
            """)

elif st.session_state.step == 5:
    st.markdown("### Step 5: Final Marketing Data Product")
    st.markdown("<p style='color: var(--text-muted); margin-bottom: 20px;'>The activated data product ready for business intelligence and marketing campaigns.</p>", unsafe_allow_html=True)
    
    if not st.session_state.model_generated:
        st.warning("Please complete Step 4 to generate the data model first.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1: metric_card("Target Audience Size", "12,450", delta="New Segment", delta_type="up")
        with c2: metric_card("Estimated Campaign ROI", "+18%", delta="Based on LTV", delta_type="up")
        with c3: metric_card("Data Quality Score", "99.9%", delta="DLP Secured", delta_type="up")
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            <div class="chart-wrap">
                <div class="chart-title">Audience Distribution by Country</div>
                <div class="chart-subtitle">High-value electronics purchasers in Europe.</div>
            """, unsafe_allow_html=True)
            
            df_chart = pd.DataFrame({
                "Country": ["UK", "Germany", "France", "Spain", "Italy"],
                "Users": [4500, 3200, 2100, 1500, 1150]
            })
            
            fig = px.bar(df_chart, x="Country", y="Users", color_discrete_sequence=["#2563eb"])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)")
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("**Sample Activated Data**")
            df_final = pd.DataFrame({
                "user_id": ["U-102", "U-455", "U-891"],
                "customer_ltv": ["$1,240", "$2,100", "$950"],
                "country": ["UK", "Germany", "France"]
            })
            render_table(df_final)
            
            st.markdown("<br/>", unsafe_allow_html=True)
            st.success("✅ **Data Product is active and ready for BigQuery integration.**")
