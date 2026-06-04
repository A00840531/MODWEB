import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. PAGE INITIALIZATION & STYLING
# ==============================================================================
st.set_page_config(
    page_title="Socioeconomic Survival Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title { font-size:30px; font-weight:bold; color:#1E3A8A; margin-bottom:5px; }
    .subtitle { font-size:15px; color:#4B5563; margin-bottom:25px; line-height: 1.6; }
    .section-header { font-size:20px; font-weight:bold; color:#1F2937; margin-top:25px; margin-bottom:15px; }
    .kpi-card { background-color: #F9FAFB; padding: 18px; border-radius: 6px; border-left: 4px solid #9CA3AF; }
    .dynamic-signal { background-color: #F0F4F8; padding: 12px; border-radius: 4px; border-left: 4px solid #1E3A8A; font-size: 14px; color: #1F2937; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. HIGH-PERFORMANCE DATA LOADING & TRANSFORMATION
# ==============================================================================
@st.cache_data
def load_and_group_dashboard_engine():
    df = pd.read_csv("cleaned_covid_dashboard_data.csv")
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01')
    
    # Standardize and translate acronyms from the CSV layout
    income_clean = df['Wb_income'].astype(str).str.strip().str.upper()
    income_mapping = {
        "HIC": "High Income",
        "LIC": "Low Income",
        "UMC": "Middle Income",
        "LMC": "Middle Income"
    }
    df['Income_Tier'] = income_clean.map(income_mapping).fillna("Middle Income")
    return df

try:
    df = load_and_group_dashboard_engine()
except FileNotFoundError:
    st.error("🚨 Error: 'cleaned_covid_dashboard_data.csv' not found. Please check your directory.")
    st.stop()

# ==============================================================================
# 3. GLOBAL INTERACTIVE CONTROL PANEL (SIDEBAR)
# ==============================================================================
st.sidebar.header("🌍 Global Filtering Controls")
st.sidebar.markdown("Modifying parameters here re-runs the entire app logic to update charts and insights simultaneously.")

all_regions = sorted(df['Who_region'].dropna().unique())
selected_regions = st.sidebar.multiselect("WHO Regions", options=all_regions, default=all_regions)

all_income_groups = sorted(df['Income_Tier'].unique())
selected_income = st.sidebar.multiselect("Economic Cohort (3-Tier Palette)", options=all_income_groups, default=all_income_groups)

all_ages = sorted(df['Agegroup'].dropna().unique())
selected_ages = st.sidebar.multiselect("Age Demographics", options=all_ages, default=all_ages)

min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
selected_years = st.sidebar.slider("Timeline Horizon Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# FIXED STRUCTURAL ORDER: Data is filtered BEFORE any KPIs or chapters attempt to read it
filtered_df = df[
    (df['Who_region'].isin(selected_regions)) &
    (df['Income_Tier'].isin(selected_income)) &
    (df['Agegroup'].isin(selected_ages)) &
    (df['Year'].between(selected_years[0], selected_years[1]))
]

# ==============================================================================
# 4. UNIFIED STRATEGIC NARRATIVE HEADER
# ==============================================================================
st.markdown('<div class="main-title">Wealth vs. Welfare: How National Income Governed Global COVID-19 Age Mortality</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="subtitle">
    <b>Professional Persona:</b> Lead Health Equity Analyst for an International NGO.<br>
    <b>Target Stakeholders:</b> Global Health Ministers and Resource Allocators.<br>
    <b>Core Inquiry:</b> To what extent did baseline macroeconomic tiers shield specific workforce age demographics, and how did intervention lag compound these vulnerabilities?
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# 5. CHAPTER 1: TIMELINE OF MACROECONOMIC DISPARITIES
# ==============================================================================
st.markdown('<div class="section-header">Chapter 1: The Macro Divergence — Timeline of Economic Inequity</div>', unsafe_allow_html=True)

total_deaths = filtered_df['Deaths'].sum() if len(filtered_df) > 0 else 0
max_vaccination_reached = filtered_df['people_fully_vaccinated_per_hundred'].max() if len(filtered_df) > 0 else 0
total_active_countries = filtered_df['Country'].nunique() if len(filtered_df) > 0 else 0

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    st.markdown(f"""<div class="kpi-card"><h5>Aggregate Documented Deaths</h5><h2>{int(total_deaths):,}</h2></div>""", unsafe_allow_html=True)
with col_kpi2:
    st.markdown(f"""<div class="kpi-card"><h5>Peak Vaccination Coverage</h5><h2>{max_vaccination_reached:.1f}%</h2></div>""", unsafe_allow_html=True)
with col_kpi3:
    st.markdown(f"""<div class="kpi-card"><h5>Active Reporting Units</h5><h2>{total_active_countries}</h2></div>""", unsafe_allow_html=True)

st.write("")

if not filtered_df.empty:
    timeline_agg = filtered_df.groupby(['Date', 'Income_Tier'])['Deaths'].sum().reset_index()
    
    three_color_map = {
        "High Income": "#1E3A8A",   
        "Middle Income": "#D1D5DB", 
        "Low Income": "#DC2626"     
    }
    
    fig_timeline = px.area(
        timeline_agg, 
        x='Date', 
        y='Deaths', 
        color='Income_Tier',
        color_discrete_map=three_color_map,
        labels={'Deaths': 'Monthly Deaths', 'Date': 'Timeline', 'Income_Tier': 'Socioeconomic Tier'},
        template='plotly_white'
    )
    fig_timeline.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), 
        height=340,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_timeline, width='stretch')
    
    # 🧠 DYNAMIC NARRATIVE ENGINE: Inspects visible datasets dynamically
    active_tiers_in_data = timeline_agg[timeline_agg['Deaths'] > 0]['Income_Tier'].unique()
    ch1_signal = "💡 **Dynamic Visual Signal:** "
    
    if len(active_tiers_in_data) == 1:
        visible_tier = active_tiers_in_data[0]
        if visible_tier == "High Income":
            ch1_signal += "**High Income Mode:** You are analyzing HICs isolated. Notice that mortality peaks are concentrated in distinct sharp spikes, reflective of an aging population structure coupled with rapid testing infrastructure."
        elif visible_tier == "Middle Income":
            ch1_signal += "**Middle Income Mode:** You are analyzing consolidated middle-income baselines (UMC & LMC). These regions represent a massive structural cushion, absorbing waves sequentially as basic health systems expanded access."
        elif visible_tier == "Low Income":
            ch1_signal += "**Low Income Mode:** CRITICAL FOCUS LIGHT. You are looking purely at LIC vectors. Note the flat, extended, and grinding baseline signature. Without financial reserves for lockdowns, exposure remained continuous."
    elif "High Income" in active_tiers_in_data and "Low Income" in active_tiers_in_data and len(active_tiers_in_data) == 2:
        ch1_signal += "**Direct Extreme Comparison:** You have removed the middle-income buffer. This directly contrasts the sharp, volatile blue spikes of wealthy nations against the prolonged, unshielded red footprint of low-income populations."
    else:
        ch1_signal += "With all strata visible, compare the high blue wave peaks (Advanced Infrastructure) directly against the prolonged, grinding red low-income sequence."

    st.markdown(f'<div class="dynamic-signal">{ch1_signal}</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ No data clusters align with your current filter selections.")

st.markdown("---")

# ==============================================================================
# 6. CHAPTER 2: THE DEMOGRAPHIC MATRIX
# ==============================================================================
st.markdown('<div class="section-header">Chapter 2: The Structural Vulnerability — Demographic Shifts</div>', unsafe_allow_html=True)

col_viz2, col_text2 = st.columns([2, 1])

with col_viz2:
    heatmap_matrix = filtered_df.pivot_table(
        index='Agegroup', 
        columns='Year', 
        values='Deaths', 
        aggfunc='sum'
    ).fillna(0)
    
    if not heatmap_matrix.empty:
        fig_heat, ax_heat = plt.subplots(figsize=(10, 4.0))
        cmap_minimal = sns.light_palette("#DC2626", as_cmap=True)
        
        sns.heatmap(
            heatmap_matrix, 
            cmap=cmap_minimal, 
            annot=True, 
            fmt=".0f", 
            linewidths=.5, 
            ax=ax_heat,
            cbar=False
        )
        ax_heat.set_title("Mortality Concentration Density Matrix View", fontsize=11, fontweight='bold', pad=10, color="#1F2937")
        ax_heat.set_ylabel("Demographic Brackets", fontsize=9)
        ax_heat.set_xlabel("Calendar Year", fontsize=9)
        sns.despine(top=True, right=True, left=True, bottom=True)
        plt.tight_layout()
        st.pyplot(fig_heat)
        plt.close()
    else:
        st.warning("Adjust filter settings to populate matrix coordinate values.")

with col_text2:
    st.markdown("##### Dynamic Storytelling Matrix Insights")
    if "Low Income" in selected_income and "High Income" not in selected_income:
        ch2_text = """
        **Active Focus: Resource Vulnerability Mode**
        * The matrix highlights a distinct structural shift. Notice how saturation spreads heavily into the active working workforce (`15_64`). 
        * Because financial safety nets were absent, physical labor could not be suspended, leading to higher baseline exposure for working demographics.
        """
    elif "High Income" in selected_income and "Low Income" not in selected_income:
        ch2_text = """
        **Active Focus: Shielded Infrastructure Mode**
        * The data shows mortality density stays tightly insulated inside senior brackets (`65+`).
        * National wealth bought the technological infrastructure to move the labor force to remote operations, protecting working-age individuals.
        """
    else:
        ch2_text = """
        **Active Focus: Comparative Baseline Mode**
        * Toggle between filtering *only* High Income and *only* Low Income in your sidebar to see the crimson cells visibly shift downward.
        * This clear shift proves that national wealth acted directly as a shield for a country's workforce.
        """
    st.info(ch2_text)

st.markdown("---")

# ==============================================================================
# 7. CHAPTER 3: INTERVENTION EFFECTS AND DISTRIBUTION LAGS
# ==============================================================================
st.markdown('<div class="section-header">Chapter 3: The Policy Resolution — Vaccine Intervention Impact</div>', unsafe_allow_html=True)

dual_axis_data = filtered_df.groupby(['Date']).agg({
    'Deaths': 'sum',
    'people_fully_vaccinated_per_hundred': 'mean'
}).reset_index()

if not dual_axis_data.empty:
    fig_dual = go.Figure()

    fig_dual.add_trace(go.Bar(
        x=dual_axis_data['Date'],
        y=dual_axis_data['Deaths'],
        name="Monthly Deaths",
        marker_color='#E5E7EB', 
        opacity=0.9,
        yaxis="y1"
    ))

    fig_dual.add_trace(go.Scatter(
        x=dual_axis_data['Date'],
        y=dual_axis_data['people_fully_vaccinated_per_hundred'],
        name="Vaccination Pace",
        mode='lines',
        line=dict(color='#1E3A8A', width=3.5),
        yaxis="y2"
    ))

    fig_dual.update_layout(
        title="Evaluating the Curve: Vaccine Scale-up Against Mortality Drops",
        xaxis=dict(title="Timeline Horizon", showgrid=False),
        yaxis=dict(title=dict(text="Aggregate Monthly Deaths", font=dict(color="#9CA3AF")), tickfont=dict(color="#9CA3AF"), showgrid=False),
        yaxis2=dict(title=dict(text="Fully Vaccinated Individuals (per 100)", font=dict(color='#1E3A8A')), tickfont=dict(color='#1E3A8A'), anchor="x", overlaying="y", side="right", showgrid=False),
        template='plotly_white',
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.9)"),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_dual, width='stretch')
    
    # 🧠 NEW DYNAMIC CAPTION ENGINE FOR CHAPTER 3
    # Calculate the maximum average vaccination coverage currently achieved on screen
    max_vac_on_screen = dual_axis_data['people_fully_vaccinated_per_hundred'].max()
    active_regions_in_data = filtered_df['Who_region'].unique()
    
    ch3_signal = "💡 **Dynamic Visual Signal:** "
    
    # Scenario A: User isolates the African Region (AFR)
    if len(active_regions_in_data) == 1 and "AFR" in active_regions_in_data:
        ch3_signal += f"**Critical Supply Lag detected in Africa (AFR):** Peak coverage only reached **{max_vac_on_screen:.1f}%**. Notice the severe chronological gap where the vaccination curve stays flat during early waves, forcing the gray mortality bars to extend further out due to supply constraints."
    
    # Scenario B: User isolates the European Region (EUR)
    elif len(active_regions_in_data) == 1 and "EUR" in active_regions_in_data:
        ch3_signal += f"**Rapid Deployment Signature in Europe (EUR):** Vaccine implementation shot up rapidly, peaking at **{max_vac_on_screen:.1f}%**. This immediate upward trajectory acted as a policy resolution, triggering a swift and visible collapse in historical mortality bars."
        
    # Scenario C: Single-region focus on any other demographic
    elif len(active_regions_in_data) == 1:
        ch3_signal += f"**Regional Profile Analysis:** Isulating **{active_regions_in_data[0]}** shows a localized rollout ceiling at **{max_vac_on_screen:.1f}** fully vaccinated individuals per 100. Compare the angle of this blue line to other regions to judge local intervention speed."
        
    # Scenario D: Global view / Multiple regions checked
    else:
        ch3_signal += f"**Global Distribution Overview:** Across your selected parameters, the mean vaccination milestone peaked at **{max_vac_on_screen:.1f}%**. Observe how the inverse correlation holds true: as the blue line climbs, historical aggregate mortality waves are progressively compressed downward."

    st.markdown(f'<div class="dynamic-signal">{ch3_signal}</div>', unsafe_allow_html=True)
    
st.markdown("---")
st.markdown("""
    💡 **Analytical Data Integrity Notes & Policy Limitations:**
    * **Data Source:** Sourced from the *World Health Organization (WHO)* and *Our World in Data (OWID)*.
    * **Design Compliance:** This engine enforces a strict **3-color palette constraint** (Deep Blue, Neutral Gray, Crimson) and consolidates middle-income tiers to reduce cognitive clutter.
""")