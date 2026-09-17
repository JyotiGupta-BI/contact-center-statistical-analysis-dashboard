import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Contact Center Operational Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for soft slate background matching chart aesthetics
# Custom CSS for page background, reduced top padding, and uniform card colors
st.markdown("""
    <style>
    /* 1. App background: Light ice-slate tint */
    [data-testid="stAppViewContainer"] {
        background-color: #eef2f6 !important;
    }

    /* 2. Reduced top padding for header alignment */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* 3. Uniform KPI & Metric Card Styling across ALL tabs */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 16px 18px !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.06) !important;
        border: 1px solid #cbd5e1 !important;
        transition: transform 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
    }

    /* Target metric values and labels for consistent color contrast */
    div[data-testid="stMetric"] label {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #1e293b !important;
    }

    /* 4. Expander and Callout Card styling matching uniform aesthetic */
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
    }
    .callout-card {
        background-color: #ffffff !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        border-left: 5px solid #1d4ed8 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        margin-bottom: 12px !important;
        font-size: 15px !important;
        color: #0f172a !important;
    }

    /* 5. Navigation tab selection styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 14px !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        background-color: #e2e8f0 !important;
        border: 1px solid #cbd5e1 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA SAFELY  ---
@st.cache_data
def load_all_sheets():
    file_path = "Contact_Center_Analysis_Outputs.xlsx"
    excel = pd.ExcelFile(file_path)
    return {sheet: excel.parse(sheet) for sheet in excel.sheet_names}

# Try loading the default file, or fall back to an uploader if missing
try:
    data = load_all_sheets()
except Exception:
    st.sidebar.warning("⚠️ Local Excel file not found.")
    uploaded_file = st.sidebar.file_uploader("Please upload your Excel file:", type=["xlsx"])
    
    if uploaded_file is not None:
        data = load_all_sheets(uploaded_file)
    else:
        st.info("👈 Please upload 'Contact_Center_Analysis_Outputs.xlsx' in the sidebar to continue.")
        st.stop()  # Pauses app execution cleanly until file is provided    

# ==========================================
# --- HEADER SECTION ---
# ==========================================

st.title("⚡ Contact Center Operational Intelligence")
st.caption("Interactive Statistical Analysis, Performance RCA & CSAT Drivers Engine")

# ==========================================
# TOP KPI ROW (Visual Cards)
# ==========================================

q1_df = data["Q1_Overall_KPIs"].set_index("Metric")["Value"]

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Call Volume", f"{int(q1_df['Total Calls']):,}")
kpi2.metric("Answer Rate", f"{q1_df['Answer Rate']:.1f}%")
kpi3.metric("Resolution Rate", f"{q1_df['Overall Resolution Rate']:.1f}%")
kpi4.metric("Avg Answer Speed", f"{q1_df['Average Speed of Answer (sec)']:.1f}s")
kpi5.metric("Avg Satisfaction", f"{q1_df['Average Satisfaction Rating']:.2f} / 5.0")

st.divider()

# --- NAVIGATION TABS (7-TAB STORYTELLING ARCHITECTURE) ---

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 1. Executive Trends & Spread",
    "👨‍💼 2. Agent Analytics & Matrix",
    "🏷️ 3. Domain Deep-Dive",
    "🎯 4. Variability & Drivers RCA",
    "🔗 5. Correlation & CSAT Drivers",
    "🤖 6. Predictive Risk Modeling",
    "💡 7. Executive Action Plan"
])

# ==========================================
# TAB 1: EXECUTIVE TRENDS & SPREAD
# ==========================================
with tab1:
    st.subheader("Monthly Performance Trends & Variability Spread")
    q3_df = data["Q3_Monthly_Trend"]
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="callout-card"><strong>Volume Overview:</strong> Answered vs. Resolved monthly progression</div>', unsafe_allow_html=True)
        fig_vol = px.bar(
            q3_df, x="Month", y=["Answered_Calls", "Resolved_Calls"],
            barmode="group", title="Monthly Answered vs. Resolved Volume",
            labels={"value": "Calls", "variable": "Metric"},
            color_discrete_sequence=["#3498db", "#2ecc71"]
        )
        fig_vol.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
            )
        fig_vol.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_vol, use_container_width=True, key="tab1_fig_vol")
        
    with col_t2:
        st.markdown('<div class="callout-card"><strong>CSAT Trajectory:</strong> Monthly customer satisfaction trend</div>', unsafe_allow_html=True)
        fig_csat_trend = px.line(
            q3_df, x="Month", y="Avg_CSAT", markers=True,
            title="Monthly CSAT Trend Trajectory",
            labels={"Avg_CSAT": "CSAT Rating (1-5)"},
            color_discrete_sequence=["#f59e0b"]
        )
        fig_csat_trend.update_traces(line=dict(width=3), marker=dict(size=8, symbol="circle"))
        fig_csat_trend.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        fig_csat_trend.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_csat_trend, use_container_width=True, key="tab1_fig_csat")

        st.markdown("### 📊 Complete Monthly Trend Breakdown")
        st.dataframe(q3_df, hide_index=True, use_container_width=True)

    st.divider()

    col_ctrl1, col_ctrl2 = st.columns([1, 3])
    with col_ctrl1:
        metric_choice = st.radio(
            "Select Metric to Analyze Spread:",
            options=["Talk Duration", "Speed of Answer"],
            index=0
        )
    
    with col_ctrl2:
        if metric_choice == "Talk Duration":
            rca_data = data["Q8_Talk_Topic_RCA"]
            
            fig_spread = go.Figure()
            for _, row in rca_data.iterrows():
                fig_spread.add_trace(go.Box(
                    name=row["Topic"],
                    q1=[row["Avg_Talk_Duration"] - 0.675 * row["Std_Dev"]],
                    median=[row["Median_Talk_Duration"]],
                    q3=[row["Avg_Talk_Duration"] + 0.675 * row["Std_Dev"]],
                    lowerfence=[row["Minimum"]],
                    upperfence=[row["Maximum"]],
                    mean=[row["Avg_Talk_Duration"]],
                    boxpoints=False
                ))
            fig_spread.update_layout(
                title="Handling Time Distribution (Min, Q1, Median, Mean, Q3, Max) by Topic",
                yaxis_title="Seconds", height=400, showlegend=False,
                margin=dict(l=20, r=20, t=50, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            fig_spread.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
            st.plotly_chart(fig_spread, use_container_width=True, key="tab1_fig_spread")
        else:
            q2_p = data["Q2_Percentiles"]
            q2_v = data["Q2_Variability"].set_index("Metric")
            
            fig_speed = go.Figure()
            fig_speed.add_trace(go.Bar(
                x=["Minimum", "Median", "Mean", "P90 Threshold", "P95 Threshold", "Maximum"],
                y=[
                    q2_v.loc["Speed of Answer", "Minimum"],
                    q2_v.loc["Speed of Answer", "Median"],
                    q2_v.loc["Speed of Answer", "Mean"],
                    q2_p.loc[q2_p["Metric"] == "Speed of Answer", "P90"].values[0],
                    q2_p.loc[q2_p["Metric"] == "Speed of Answer", "P95"].values[0],
                    q2_v.loc["Speed of Answer", "Maximum"]
                ],
                marker_color=["#2ecc71", "#3498db", "#2980b9", "#f39c12", "#e67e22", "#e74c3c"],
                texttemplate="%{y:.1f}s", textposition="outside"
            ))
            fig_speed.update_layout(
                title="Speed of Answer Operational Spread & SLA Percentile Thresholds (Seconds)",
                yaxis_title="Seconds", height=400,
                margin=dict(l=20, r=20, t=50, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            fig_speed.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
            st.plotly_chart(fig_speed, use_container_width=True, key="tab1_fig_speed")

# ==========================================
# TAB 2: AGENT ANALYTICS & MATRIX
# ==========================================
with tab2:
    st.subheader("👨‍💼 Comprehensive Agent Operational Benchmarks")
    st.caption("Comparing individual agent resolution rates, handling times, and CSAT metrics.")

    agent_df = data["Q4_Agent_Analysis"].sort_values("Resolution_Rate_%", ascending=False)
    agent_bench = data["Q4_Agent_Benchmark"].set_index("Metric")["Overall Benchmark"]

    col_ab1, col_ab2, col_ab3, col_ab4 = st.columns(4)
    col_ab1.metric("Top Performing Agent", agent_df.iloc[0]["Agent"], f"{agent_df.iloc[0]['Resolution_Rate_%']:.1f}% Res Rate")
    col_ab2.metric("Overall Resolution Benchmark", f"{agent_bench['Resolution Rate']:.2f}%")
    col_ab3.metric("Avg Handling Time Benchmark", f"{agent_bench['Average Talk Duration']:.1f}s")
    col_ab4.metric("Avg CSAT Benchmark", f"{agent_bench['Average CSAT']:.2f}")

    st.markdown("---")

    col_ag1, col_ag2 = st.columns(2)
    with col_ag1:
        fig_agent_res = px.bar(
            agent_df.sort_values("Resolution_Rate_%", ascending=True),
            x="Resolution_Rate_%", y="Agent", orientation="h",
            text="Resolution_Rate_%", title="Agent Resolution Rate (%) vs. Benchmark",
            color="Resolution_Rate_%", color_continuous_scale="Blues"
        )
        fig_agent_res.add_vline(x=agent_bench["Resolution Rate"], line_dash="dash", line_color="red", annotation_text="Benchmark")
        fig_agent_res.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_agent_res.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        fig_agent_res.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_agent_res, use_container_width=True, key="tab2_fig_agent_res")

    with col_ag2:
        fig_agent_csat = px.scatter(
            agent_df, 
            x="Resolution_Rate_%", 
            y="Avg_CSAT", 
            text="Agent",
            size="Answered_Calls", 
            color="Avg_CSAT",
            title="Agent Efficiency vs. CSAT Matrix (Bubble Size = Call Volume)",
            labels={"Resolution_Rate_%": "Resolution Rate (%)", "Avg_CSAT": "Average CSAT"}
        )
        
        fig_agent_csat.add_hline(y=agent_bench["Average CSAT"], line_dash="dash", line_color="#94a3b8")
        fig_agent_csat.add_vline(x=agent_bench["Resolution Rate"], line_dash="dash", line_color="#94a3b8")
        fig_agent_csat.update_traces(textposition="top center")
        fig_agent_csat.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        fig_agent_csat.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
        fig_agent_csat.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_agent_csat, use_container_width=True, key="tab2_fig_agent_csat")

    st.markdown("### 📊 Agent Performance Summary Matrix")
    st.dataframe(agent_df, hide_index=True, use_container_width=True)

# ==========================================
# TAB 3: DOMAIN (TOPIC) DEEP-DIVE
# ==========================================
with tab3:
    st.subheader("🏷️ Domain & Call Topic Breakdown")
    st.caption("Analyzing operational performance, issue complexity, and resolution across functional domains.")

    topic_df = data["Q5_Topic_Analysis"].sort_values("Answered_Calls", ascending=False)

    col_tp1, col_tp2, col_tp3 = st.columns(3)
    col_tp1.metric("Highest Volume Domain", topic_df.iloc[0]["Topic"], f"{topic_df.iloc[0]['Answered_Calls']} Calls")
    col_tp2.metric("Lowest Resolution Domain", "Streaming", "88.43% Res Rate")
    col_tp3.metric("Longest Handling Domain", "Admin Support", "228.05s Avg Duration")

    st.markdown("---")

    col_top1, col_top2 = st.columns(2)
    with col_top1:
        fig_topic_vol = px.bar(
            topic_df, x="Topic", y="Answered_Calls",
            title="Call Volume Distribution across Domains",
            color="Answered_Calls", color_continuous_scale="Oranges",
            text="Answered_Calls"
        )
        fig_topic_vol.update_traces(textposition='outside')
        fig_topic_vol.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        fig_topic_vol.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_topic_vol, use_container_width=True, key="tab3_fig_topic_vol")

    with col_top2:
        fig_topic_res = px.bar(
            topic_df.sort_values("Resolution_Rate_%", ascending=True),
            x="Resolution_Rate_%", y="Topic", orientation="h",
            title="Domain Resolution Rates (%)",
            color="Resolution_Rate_%", color_continuous_scale="Greens",
            text="Resolution_Rate_%"
        )
        fig_topic_res.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_topic_res.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        fig_topic_res.update_xaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_topic_res, use_container_width=True, key="tab3_fig_topic_res")

# ==========================================
# TAB 4: VARIABILITY & DRIVERS RCA
# ==========================================
with tab4:
    st.subheader("🔍 Root Cause Analysis (RCA): Process Drivers & Variability")
    st.caption("Investigating handling time dispersion, outlier skewness, and extreme SLA thresholds.")

    rca_data = data["Q8_Talk_Topic_RCA"].set_index("Topic")

    st.markdown("### ⏱️ Talk Duration Dispersion Across Domains")
    fig_topic_box = go.Figure()
    for topic_name, row in rca_data.iterrows():
        fig_topic_box.add_trace(go.Box(
            name=topic_name,
            q1=[row["Avg_Talk_Duration"] - 0.675 * row["Std_Dev"]],
            median=[row["Median_Talk_Duration"]],
            q3=[row["Avg_Talk_Duration"] + 0.675 * row["Std_Dev"]],
            lowerfence=[row["Minimum"]],
            upperfence=[row["Maximum"]],
            mean=[row["Avg_Talk_Duration"]],
            boxpoints=False
        ))
    fig_topic_box.update_layout(
        title="Domain Handling Time Spread (Min, Median, Mean, Max in Seconds)",
        yaxis_title="Seconds", height=420,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    fig_topic_box.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
    st.plotly_chart(fig_topic_box, use_container_width=True, key="tab4_fig_rca_box")

    st.markdown("---")

    col_rca1, col_rca2 = st.columns([1, 2])
    with col_rca1:
        st.markdown("### 🚦 Speed of Answer Tail Risk")
        st.info("""
        * **P90 Threshold:** 90% of callers wait within **39s**.
        * **P95 Threshold:** 95% of callers wait within **52s**.
        * **Max Spike:** Extreme queue outliers reach up to **113s**.
        * **RCA Verdict:** Standard average speed (19.8s) masks long-tail queue bottlenecks experienced during peak arrival hours.
        """)
        
    with col_rca2:
        q2_p = data["Q2_Percentiles"]
        q2_v = data["Q2_Variability"].set_index("Metric")
        
        fig_speed_rca = go.Figure()
        fig_speed_rca.add_trace(go.Bar(
            x=["Minimum", "Median", "Mean", "P90 Threshold", "P95 Threshold", "Maximum"],
            y=[
                q2_v.loc["Speed of Answer", "Minimum"],
                q2_v.loc["Speed of Answer", "Median"],
                q2_v.loc["Speed of Answer", "Mean"],
                q2_p.loc[q2_p["Metric"] == "Speed of Answer", "P90"].values[0],
                q2_p.loc[q2_p["Metric"] == "Speed of Answer", "P95"].values[0],
                q2_v.loc["Speed of Answer", "Maximum"]
            ],
            marker_color=["#2ecc71", "#3498db", "#2980b9", "#f39c12", "#e67e22", "#e74c3c"],
            texttemplate="%{y:.1f}s", textposition="outside"
        ))
        fig_speed_rca.update_layout(
            title="Speed of Answer Percentile Distribution (Seconds)",
            yaxis_title="Seconds", height=380,
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        fig_speed_rca.update_yaxes(showgrid=True, gridcolor="#f1f5f9")
        st.plotly_chart(fig_speed_rca, use_container_width=True, key="tab4_fig_speed_rca")

# ==========================================
# TAB 5: CORRELATION & CSAT DRIVERS
# ==========================================
with tab5:
    st.subheader("🔗 Statistical Correlation & CSAT Drivers")
    st.caption("Measuring linear relationships between operational metrics and CSAT.")

    col_c1, col_c2 = st.columns([1, 2])
    
    with col_c1:
        st.markdown("### 💡 Key Statistical Takeaways")
        st.info("""
        * **Speed of Answer vs. CSAT (`r = 0.001`):** No statistically significant correlation. Queue time does not drive satisfaction.
        * **Talk Duration vs. CSAT (`r = 0.000`):** Call length has zero correlation with satisfaction scores.
        * **Resolution vs. CSAT (`r = 0.120`):** First-contact resolution remains the strongest operational driver of CSAT.
        * **Management Action:** Shift core operational KPIs away from Average Handling Time (AHT) toward First Contact Resolution (FCR).
        """)

    with col_c2:
        corr_matrix = pd.DataFrame(
            [[1.000, -0.003, 0.001, 0.007],
             [-0.003, 1.000, 0.000, 0.007],
             [0.001, 0.000, 1.000, 0.120],
             [0.007, 0.007, 0.120, 1.000]],
            index=["Speed of Answer", "Talk Duration", "CSAT Rating", "Resolved"],
            columns=["Speed of Answer", "Talk Duration", "CSAT Rating", "Resolved"]
        )
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".3f",
            color_continuous_scale="RdBu_r",
            title="Operational Metrics Correlation Matrix",
            aspect="auto"
        )
        fig_corr.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_corr, use_container_width=True, key="tab5_fig_corr")

# ==========================================
# TAB 6: PREDICTIVE MODELING
# ==========================================
with tab6:
    st.subheader("🤖 Low Satisfaction Predictive Modeling & Features")
    st.caption("Evaluating machine learning models to identify at-risk callers early.")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("#### Classification Model Metrics")
        st.dataframe(data["Q9_Predictive_Model"], hide_index=True, use_container_width=True)

    with col_m2:
        st.markdown("#### Recommended Features for Model Expansion")
        st.dataframe(data["Q9_Additional_Data"], hide_index=True, use_container_width=True)

# ==========================================
# TAB 7: MANAGEMENT ACTION PLAN
# ==========================================
with tab7:
    st.subheader("💡 Executive Insights & Recommended Actions")

    action_df = data["Q10_Action_Plan"]

    for idx, row in action_df.iterrows():
        with st.expander(f"📌 Key Finding {idx+1}: {row['Finding']}", expanded=True):
            col_e1, col_e2 = st.columns([1, 2])
            with col_e1:
                st.info(f"**Supporting Evidence:**\n\n{row['Evidence']}")
            with col_e2:
                st.success(f"**Action Required:**\n\n{row['Management_Action']}")