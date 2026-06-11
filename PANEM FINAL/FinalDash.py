import streamlit as st
import pandas as pd
import plotly.express as px
import os
import html
import json
from pathlib import Path

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="PANEM",
    layout="wide"
)

# =====================================================
# STYLE
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFCF3;
        color: #2f2a26;
        font-family: "Courier New", monospace;
    }

    html, body, [class*="css"] {
        font-family: "Courier New", monospace !important;
        color: #2f2a26;
    }

    section[data-testid="stSidebar"] {
        background-color: #F3E9D2;
        border-right: 1px solid #d6c09a;
    }

    section[data-testid="stSidebar"] * {
        font-family: "Courier New", monospace !important;
        color: #2f2a26 !important;
    }

    [data-baseweb="tag"] {
        background-color: #e6d3b3 !important;
        color: #2f2a26 !important;
        border-radius: 6px !important;
        border: 1px solid #c7a982 !important;
        font-family: "Courier New", monospace !important;
    }

    [data-baseweb="tag"] svg {
        color: #2f2a26 !important;
        fill: #2f2a26 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #fff7e8 !important;
        border-color: #d8c3a5 !important;
        color: #2f2a26 !important;
        font-family: "Courier New", monospace !important;
    }

    input, textarea, select {
        font-family: "Courier New", monospace !important;
    }

    .panem-note {
        background-color: #fff7e8;
        border-left: 6px solid #8b6f47;
        padding: 14px 18px;
        border-radius: 4px;
        margin-bottom: 24px;
        font-size: 16px;
        color: #2f2a26;
        font-family: "Courier New", monospace;
    }

    .instruction-box {
        background-color: #fff7e8;
        border-left: 6px solid #8b6f47;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 14px;
        font-size: 16px;
        color: #2f2a26;
        font-family: "Courier New", monospace;
    }

    .instruction-box b {
        color: #5c432d;
    }

    .alert-positive {
        background-color: #edf7ed;
        border: 1px solid #95c995;
        border-left: 7px solid #2f7d32;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 12px;
        font-size: 15px;
        color: #1f4f22;
        font-family: "Courier New", monospace;
    }

    .alert-negative {
        background-color: #fdeaea;
        border: 1px solid #df9b9b;
        border-left: 7px solid #b23b3b;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 12px;
        font-size: 15px;
        color: #7d2525;
        font-family: "Courier New", monospace;
    }

    .branch-legend {
        background-color: #fff7e8;
        border: 1px solid #d8c3a5;
        border-radius: 8px;
        padding: 12px 14px;
        margin-top: 12px;
        margin-bottom: 16px;
        font-size: 14px;
    }

    .branch-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    .branch-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-block;
        border: 1px solid rgba(0,0,0,0.15);
    }

    h1, h2, h3 {
        color: #2f2a26 !important;
        font-family: "Courier New", monospace !important;
    }

    div[data-testid="stMetric"] {
        background-color: #fff7e8;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #d8c3a5;
        box-shadow: 0px 2px 8px rgba(92, 67, 45, 0.08);
        font-family: "Courier New", monospace !important;
    }

    div[data-testid="stMetric"] * {
        font-family: "Courier New", monospace !important;
    }

    .kpi-card {
        background-color: #fff7e8;
        padding: 18px 22px;
        border-radius: 10px;
        border: 1px solid #d8c3a5;
        box-shadow: 0px 2px 8px rgba(92, 67, 45, 0.08);
        font-family: "Courier New", monospace !important;
        min-height: 145px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        white-space: normal !important;
        overflow: visible !important;
    }

    .kpi-label {
        color: #6b5a45;
        font-size: 15px;
        font-weight: 600;
        line-height: 1.25;
        margin-bottom: 12px;
        white-space: normal !important;
    }

    .kpi-value {
        color: #2f2a26;
        font-size: clamp(22px, 2.0vw, 38px);
        font-weight: 600;
        line-height: 1.12;
        white-space: normal !important;
        overflow-wrap: anywhere;
        word-break: normal;
    }

    .kpi-value.long-value {
        font-size: clamp(18px, 1.45vw, 28px);
        line-height: 1.2;
    }

    div[data-testid="stExpander"] {
        background-color: #fff7e8;
        border-radius: 10px;
        border: 1px solid #d8c3a5;
        font-family: "Courier New", monospace !important;
    }

    .block-container {
        padding-top: 2rem;
    }

    /* Conversational Chat Component Styles */
    .chat-bubble-user {
        background-color: #e6d3b3;
        color: #2f2a26;
        padding: 12px 16px;
        border-radius: 15px 15px 0px 15px;
        margin-bottom: 10px;
        max-width: 75%;
        margin-left: auto;
        border: 1px solid #c7a982;
    }
    .chat-bubble-bot {
        background-color: #fff7e8;
        color: #2f2a26;
        padding: 12px 16px;
        border-radius: 15px 15px 15px 0px;
        margin-bottom: 10px;
        max-width: 75%;
        margin-right: auto;
        border: 1px solid #d8c3a5;
    }
    .live-navigation-box {
        background-color: #fff7e8;
        border: 1px dashed #8b6f47;
        border-radius: 8px;
        padding: 14px;
        margin-top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def clean_name(value):
    if pd.isna(value):
        return value

    value = str(value).strip()

    if value.lower().startswith("data"):
        value = value[4:]

    value = value.replace("_", " ")
    value = value.replace("-", " ")
    value = value.strip()

    return value.title()


def clean_columns(df):
    df.columns = df.columns.str.strip()
    return df


def format_date_column(df, column):
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


def apply_plot_theme(fig):
    fig.update_layout(
        paper_bgcolor="#FFFCF3",
        plot_bgcolor="#FFFCF3",
        font=dict(
            family="Courier New, monospace",
            color="#2f2a26",
            size=13
        ),
        title=dict(
            font=dict(size=18, color="#2f2a26"),
            x=0.02
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            title_font=dict(color="#2f2a26"),
            tickfont=dict(color="#6b5a45")
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            title_font=dict(color="#2f2a26"),
            tickfont=dict(color="#6b5a45")
        ),
        legend=dict(
            bgcolor="rgba(255,252,243,0)",
            font=dict(color="#2f2a26")
        ),
        margin=dict(l=40, r=30, t=70, b=40)
    )
    return fig


def confidence_label(avg_percentage_error):
    if pd.isna(avg_percentage_error):
        return "Unknown"

    if avg_percentage_error <= 15:
        return "High confidence"

    if avg_percentage_error <= 30:
        return "Medium confidence"

    return "Low confidence"


def alert_message(row):
    product = row["product"]
    predicted = row["predicted"]
    baseline = row["historical_baseline"]
    error = row["percentage_error"]

    alerts = []

    if not pd.isna(baseline) and baseline > 0:
        difference = ((predicted - baseline) / baseline) * 100

        if difference >= 20:
            alerts.append(
                {
                    "type": "positive",
                    "message": f"High demand alert for {product}: predicted sales are {difference:.1f}% above the historical baseline."
                }
            )

        elif difference <= -20:
            alerts.append(
                {
                    "type": "negative",
                    "message": f"Low demand alert for {product}: predicted sales are {abs(difference):.1f}% below the historical baseline."
                }
            )

    if not pd.isna(error) and error > 30:
        alerts.append(
            {
                "type": "negative",
                "message": f"Low confidence alert for {product}: recent error is high, so use this forecast carefully."
            }
        )

    return alerts


def style_table(df):
    return (
        df.style
        .set_properties(
            **{
                "background-color": "#fff7e8",
                "color": "#2f2a26",
                "border-color": "#d8c3a5",
                "font-family": "Courier New, monospace"
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#c8ae87"),
                        ("color", "#2f2a26"),
                        ("font-family", "Courier New, monospace"),
                        ("border-color", "#d8c3a5")
                    ]
                },
                {
                    "selector": "td",
                    "props": [
                        ("border-color", "#d8c3a5"),
                        ("font-family", "Courier New, monospace")
                    ]
                }
            ]
        )
    )


def render_branch_legend(branches, branch_color_map):
    legend_html = "<div class='branch-legend'><b>Branch color key</b><br><br>"

    for branch in branches:
        color = branch_color_map.get(branch, "#c8ae87")

        legend_html += (
            "<div class='branch-row'>"
            f"<span class='branch-dot' style='background-color:{color};'></span>"
            f"<span>{branch}</span>"
            "</div>"
        )

    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)


def add_product_highlight(df, value_col):
    top_product_value = df[value_col].max()

    df["product_highlight"] = df[value_col].apply(
        lambda x: "Top product" if x == top_product_value else "Other products"
    )
    return df


def render_kpi_card(container, label, value):
    value_text = str(value)
    label_text = str(label)
    long_class = " long-value" if len(value_text) > 14 else ""

    container.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{html.escape(label_text)}</div>
            <div class="kpi-value{long_class}">{html.escape(value_text)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# LOCAL QUERY PARSER (Replaces OpenAI Copilot Engine)
# =====================================================
def get_local_copilot_response(query):
    """
    Parses incoming manager queries locally and returns a structured response map 
    and dashboard page navigation alignment.
    """
    q = query.lower().strip()
    
    # 1. Branch Forecast / Target questions
    if "forecast" in q or "target" in q or "predict" in q or "allocation" in q or "demand" in q:
        return {
            "response": "To view your future operational constraints and production targets, use the <b>Branch Forecast</b> tab. Here you can filter by specific branch and prediction dates to optimize baking workflows, review calculated revenue adjustments, and react to high/low demand alerts.",
            "suggestedPage": "Branch Forecast"
        }
    
    # 2. Historical patterns or past sales questions
    elif "history" in q or "past" in q or "historical" in q or "pattern" in q or "sold" in q or "sales" in q:
        return {
            "response": "To map past customer behaviors and historical transaction trends across the network, please use the <b>Historical Sales</b> tab. You can multi-filter across multiple locations, explore high-volume categories, or view volume variance segmented by days of the week.",
            "suggestedPage": "Historical Sales"
        }
        
    # 3. Model validation, accuracy, trust, metrics or error terms
    elif "trust" in q or "mape" in q or "mae" in q or "error" in q or "accuracy" in q or "reliable" in q or "confidence" in q:
        return {
            "response": "For evaluating forecasting reliability, head over to the <b>Model Trust</b> tab. This view translates numerical baseline errors (MAPE / MAE footprints) into direct labels like 'High/Medium/Low confidence' so you can gauge production risks safely.",
            "suggestedPage": "Model Trust"
        }
        
    # 4. Sheets updating, data replacement or overlap issues
    elif "update" in q or "sheet" in q or "upload" in q or "excel" in q or "csv" in q or "overlap" in q:
        return {
            "response": "To incorporate fresh data into the pipeline, switch over to the <b>Update Data</b> view. This space allows you to upload external CSV or Excel logs, automatically vetting dates for overlaps with legacy historical windows before engine retraining.",
            "suggestedPage": "Update Data"
        }
        
    # 5. Technical features or inner metrics details
    elif "technical" in q or "feature" in q or "importance" in q or "weekly" in q or "engine" in q:
        return {
            "response": "The <b>Technical Details</b> section contains granular metrics for engineers. It shows chronological weekly error lines alongside machine learning feature importances to describe which attributes drive model behaviors.",
            "suggestedPage": "Technical Details"
        }
        
    # Default fallback response
    return {
        "response": "Hello Manager! I can guide you through our system metrics. Try asking questions containing terms like <b>'forecast'</b>, <b>'historical sales'</b>, <b>'model error (MAPE)'</b>, or <b>'updating sheets'</b> to dynamically focus your view context.",
        "suggestedPage": None
    }


# =====================================================
# PATH CONFIGURATION & LOAD EXCEL DATASOURCE
# =====================================================

SCRIPT_DIR = Path(__file__).parent
excel_file = SCRIPT_DIR / "Panem_Dashboard_Datasource.xlsx"

if not excel_file.exists():
    st.error(f"Excel file not found at: {excel_file.resolve()}. Please place 'Panem_Dashboard_Datasource.xlsx' in the exact same folder as this app script.")
    st.stop()

daily_sales = clean_columns(pd.read_excel(excel_file, sheet_name="Daily_Sales"))
model_results = clean_columns(pd.read_excel(excel_file, sheet_name="Model_Results"))
weekly_errors = clean_columns(pd.read_excel(excel_file, sheet_name="Weekly_Errors"))
rolling_forecast = clean_columns(pd.read_excel(excel_file, sheet_name="Rolling_Forecast"))

try:
    feature_importance = clean_columns(pd.read_excel(excel_file, sheet_name="Feature_Importance"))
except:
    feature_importance = pd.DataFrame()

# =====================================================
# PREPARE DATA
# =====================================================

daily_sales = format_date_column(daily_sales, "operating_date")
rolling_forecast = format_date_column(rolling_forecast, "date")

daily_sales = daily_sales.dropna(subset=["operating_date"])
rolling_forecast = rolling_forecast.dropna(subset=["date"])

daily_sales["branch"] = daily_sales["branch"].apply(clean_name)
daily_sales["item"] = daily_sales["item"].apply(clean_name)

model_results["product"] = model_results["product"].apply(clean_name)
weekly_errors["product"] = weekly_errors["product"].apply(clean_name)

rolling_forecast["product"] = rolling_forecast["product"].apply(clean_name)
rolling_forecast["branch"] = rolling_forecast["branch"].apply(clean_name)

if not feature_importance.empty:
    feature_importance["product"] = feature_importance["product"].apply(clean_name)

if "day_of_week" not in daily_sales.columns:
    daily_sales["day_of_week"] = daily_sales["operating_date"].dt.dayofweek

day_names = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

daily_sales["day_name"] = daily_sales["day_of_week"].map(day_names)

# =====================================================
# MAKE OLD AND NEW EXCEL VERSIONS COMPATIBLE
# =====================================================

if "Baseline_MAE" not in model_results.columns and "Historical_MAE" in model_results.columns:
    model_results["Baseline_MAE"] = model_results["Historical_MAE"]

if "Baseline_MAPE" not in model_results.columns and "Historical_MAPE" in model_results.columns:
    model_results["Baseline_MAPE"] = model_results["Historical_MAPE"]

if "MAE_Improvement_%" not in model_results.columns and "Historical_MAE_Improvement_%" in model_results.columns:
    model_results["MAE_Improvement_%"] = model_results["Historical_MAE_Improvement_%"]

if "MAPE_Improvement_%" not in model_results.columns and "Historical_MAPE_Improvement_%" in model_results.columns:
    model_results["MAPE_Improvement_%"] = model_results["Historical_MAPE_Improvement_%"]

# =====================================================
# COLORS
# =====================================================

branch_color_map = {
    "Punto Valle": "#a97c55",
    "Qin": "#6f8f72",
    "Zambrano": "#a65f46",
    "Kavia": "#b09163",
    "Nativa": "#c8ae87",
    "Carreta": "#5c432d",
    "Credi Club": "#8b6f47"
}

fallback_branch_palette = [
    "#7b6d8d",
    "#b57f50",
    "#4f6f52",
    "#9c7352",
    "#b09163"
]

all_branches = sorted(
    set(daily_sales["branch"].dropna().unique()).union(
        set(rolling_forecast["branch"].dropna().unique())
    )
)

for i, branch in enumerate(all_branches):
    if branch not in branch_color_map:
        branch_color_map[branch] = fallback_branch_palette[i % len(fallback_branch_palette)]

product_base_color = "#e6d3b3"
product_highlight_color = "#7a4f2f"

product_color_map = {
    "Top product": product_highlight_color,
    "Other products": product_base_color
}

base_color = "#c8ae87"
soft_color = "#dfc9a7"
highlight_color = "#5c432d"
positive_color = "#2f7d32"
negative_color = "#b23b3b"

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

logo_path = SCRIPT_DIR / "panem_logo.png"

if logo_path.exists():
    st.sidebar.image(str(logo_path), width="stretch")
else:
    st.sidebar.markdown("## PANEM")

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Select page",
    [
        "1. Branch Forecast",
        "2. Historical Sales",
        "3. Model Trust",
        "4. Update Data",
        "5. Technical Details"
    ]
)

# =====================================================
# PAGE 1: BRANCH FORECAST & DATA COPILOT
# =====================================================

if page == "1. Branch Forecast":

    st.header("Branch Forecast")

    st.markdown(
        """
        <div class="panem-note">
            Main view for branch leaders. Select your branch and review the expected product demand for the next seven prediction days.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    selected_branch = col1.selectbox(
        "Select branch",
        options=sorted(rolling_forecast["branch"].dropna().unique())
    )

    available_dates = (
        rolling_forecast[rolling_forecast["branch"] == selected_branch]["date"]
        .dropna()
        .sort_values()
        .dt.strftime("%Y-%m-%d")
        .unique()
        .tolist()
    )

    if len(available_dates) == 0:
        st.warning("No prediction dates available for this branch.")
        st.stop()

    selected_start_date = col2.selectbox(
        "Prediction start date",
        options=available_dates
    )

    selected_start_date = pd.to_datetime(selected_start_date)

    unit_price = col3.number_input(
        "Estimated unit price",
        min_value=1.0,
        value=50.0,
        step=1.0
    )

    render_branch_legend([selected_branch], branch_color_map)

    branch_forecast = rolling_forecast[
        (rolling_forecast["branch"] == selected_branch) &
        (rolling_forecast["date"] >= selected_start_date)
    ].copy()

    branch_forecast = branch_forecast.sort_values(["date", "product"])

    selected_dates = (
        branch_forecast["date"]
        .drop_duplicates()
        .sort_values()
        .head(7)
    )

    forecast_window = branch_forecast[
        branch_forecast["date"].isin(selected_dates)
    ].copy()

    if forecast_window.empty:
        st.warning("No forecast data available for this branch and start date.")
        st.stop()

    agg_dict = {
        "predicted": ("predicted", "sum"),
        "actual": ("actual", "sum"),
        "historical_baseline": ("historical_baseline", "sum"),
        "absolute_error": ("absolute_error", "mean"),
        "percentage_error": ("percentage_error", "mean")
    }

    if "recent_7_day_baseline" in forecast_window.columns:
        agg_dict["recent_7_day_baseline"] = ("recent_7_day_baseline", "sum")

    product_summary = (
        forecast_window
        .groupby("product")
        .agg(**agg_dict)
        .reset_index()
    )

    product_summary["difference_vs_baseline"] = (
        product_summary["predicted"] - product_summary["historical_baseline"]
    )

    product_summary["confidence"] = product_summary["percentage_error"].apply(confidence_label)
    product_summary["forecasted_revenue"] = product_summary["predicted"] * unit_price

    total_predicted_units = product_summary["predicted"].sum()
    total_revenue = product_summary["forecasted_revenue"].sum()
    top_product = product_summary.sort_values("predicted", ascending=False).iloc[0]["product"]
    average_error = product_summary["percentage_error"].mean()
    confidence = confidence_label(average_error)

    st.subheader("Next 7 Days Prediction")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        render_kpi_card(st, "Predicted Units", f"{total_predicted_units:,.0f}")
    with kpi2:
        display_prod = top_product if len(top_product) <= 18 else f"{top_product[:15]}..."
        render_kpi_card(st, "Top Product Target", display_prod)
    with kpi3:
        render_kpi_card(st, "Estimated Revenue", f"${total_revenue:,.2f}")
    with kpi4:
        render_kpi_card(st, "Forecast Confidence", confidence)

    st.subheader("Alerts")

    all_alerts = []
    for _, row in product_summary.iterrows():
        all_alerts.extend(alert_message(row))

    if len(all_alerts) == 0:
        st.markdown(
            """
            <div class="alert-positive">
                No major alerts for this branch. Forecasted demand is close to the historical baseline and model error is within a reasonable range.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        for alert in all_alerts:
            css_class = "alert-positive" if alert["type"] == "positive" else "alert-negative"
            st.markdown(
                f"""
                <div class="{css_class}">
                    {alert["message"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.subheader("Product Forecast")

    product_summary = product_summary.sort_values("predicted", ascending=False)
    product_summary = add_product_highlight(product_summary, "predicted")

    fig_products = px.bar(
        product_summary,
        x="predicted",
        y="product",
        color="product_highlight",
        orientation="h",
        color_discrete_map=product_color_map,
        title=f"Expected Demand Allocation — {selected_branch}",
        text_auto=".0f"
    )

    fig_products.update_layout(
        showlegend=False,
        hovermode="y unified"
    )
    fig_products.update_yaxes(categoryorder="total ascending", title="")
    fig_products.update_xaxes(title="Predicted Volumes (Units)")
    fig_products.update_traces(
        textposition="outside",
        textfont=dict(color="#2f2a26", size=11),
        marker=dict(line=dict(color="#2f2a26", width=1))
    )
    fig_products = apply_plot_theme(fig_products)

    st.plotly_chart(fig_products, use_container_width=True)

    st.subheader("Monthly Context")

    forecast_month = selected_start_date.month

    monthly_context = daily_sales[
        (daily_sales["branch"] == selected_branch) &
        (daily_sales["operating_date"].dt.month == forecast_month)
    ].copy()

    if not monthly_context.empty:
        monthly_product_sales = (
            monthly_context
            .groupby("item")["quantity"]
            .sum()
            .reset_index()
            .sort_values("quantity", ascending=False)
        )

        monthly_product_sales = add_product_highlight(
            monthly_product_sales,
            "quantity"
        )

        fig_month = px.bar(
            monthly_product_sales,
            x="quantity",
            y="item",
            color="product_highlight",
            orientation="h",
            color_discrete_map=product_color_map,
            title=f"What usually sells in {selected_branch} during the forecast month",
            text_auto=True
        )

        fig_month.update_layout(showlegend=False, hovermode="y unified")
        fig_month.update_yaxes(categoryorder="total ascending", title="")
        fig_month.update_xaxes(title="Historical Volumes (Units)")
        fig_month.update_traces(
            textposition="outside",
            textfont_color="#2f2a26",
            marker=dict(line=dict(color="#2f2a26", width=1))
        )
        fig_month = apply_plot_theme(fig_month)

        st.plotly_chart(fig_month, use_container_width=True)

    decision_columns = ["product", "predicted", "historical_baseline"]
    if "recent_7_day_baseline" in product_summary.columns:
        decision_columns.append("recent_7_day_baseline")

    decision_columns += ["difference_vs_baseline", "percentage_error", "confidence", "forecasted_revenue"]

    decision_table = product_summary[decision_columns].copy()
    decision_table = decision_table.rename(
        columns={
            "product": "Product",
            "predicted": "Predicted units",
            "historical_baseline": "Historical baseline",
            "recent_7_day_baseline": "Recent 7-day baseline",
            "difference_vs_baseline": "Difference vs historical baseline",
            "percentage_error": "Average error %",
            "confidence": "Confidence",
            "forecasted_revenue": "Estimated revenue"
        }
    )

    with st.expander("View Forecast Table for Decision Making"):
        st.dataframe(style_table(decision_table), use_container_width=True)

    # =====================================================
    # LOCAL OFFLINE COPILOT NAVIGATION COMPONENT
    # =====================================================
    st.markdown("---")
    st.subheader("👨🏼‍🍳 Panem Operational Analytics Copilot")
    
    if "copilot_messages" not in st.session_state:
        st.session_state["copilot_messages"] = [
            {"role": "assistant", "content": "Hello Team Panem! I am your dashboard data assistant. I can help you interpret demand forecasts, break down model error flags, or guide you to data update views. What operational metrics can I help you with?"}
        ]
    if "active_navigation_hint" not in st.session_state:
        st.session_state["active_navigation_hint"] = None

    chat_col, guide_col = st.columns([2, 1])

    with chat_col:
        for msg in st.session_state["copilot_messages"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-bubble-user">{html.escape(msg["content"])}</div>', unsafe_allow_html=True)
            else:
                # Allow minor internal HTML blocks (like bolded recommendations) from our local dictionary
                formatted_bot_text = msg["content"].replace("\n", "<br>")
                st.markdown(f'<div class="chat-bubble-bot">{formatted_bot_text}</div>', unsafe_allow_html=True)

        user_query = st.chat_input("Ask about forecasts, error metrics, or sheets...")
        
        if user_query:
            st.markdown(f'<div class="chat-bubble-user">{html.escape(user_query)}</div>', unsafe_allow_html=True)
            st.session_state["copilot_messages"].append({"role": "user", "content": user_query})

            # Fetch local evaluation maps completely offline without calling OpenAI
            local_result = get_local_copilot_response(user_query)
            
            st.session_state["active_navigation_hint"] = local_result["suggestedPage"]
            st.session_state["copilot_messages"].append({"role": "assistant", "content": local_result["response"]})
            st.rerun()

    with guide_col:
        st.markdown("<div class='live-navigation-box'>", unsafe_allow_html=True)
        st.markdown("🗺️ **Dashboard Map & Context**")
        
        current_hint = st.session_state["active_navigation_hint"]
        if current_hint:
            st.markdown(f"**Recommended Dashboard Tab:**\n`{current_hint}`")
            st.markdown("Please switch to this page using the navigation sidebar on the left to see the charts.")
        else:
            st.markdown("<span style='color: #6b5a45; font-size:13px;'>Ask me how to find specific insights or read metrics!</span>", unsafe_allow_html=True)
            
        st.markdown("---")
        if st.button("Reset Assistant Logs", use_container_width=True):
            st.session_state["copilot_messages"] = [
                {"role": "assistant", "content": "Hello Team Panem! 🥐 I am your dashboard data assistant. I can help you interpret demand forecasts, break down model error flags, or guide you to data update views. What operational metrics can I help you with?"}
            ]
            st.session_state["active_navigation_hint"] = None
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# PAGE 2: HISTORICAL SALES
# =====================================================

elif page == "2. Historical Sales":

    st.header("Historical Sales Overview")

    st.markdown(
        """
        <div class="panem-note">
            This page shows past demand patterns by branch, product, and date. Branches use consistent colors for easier identification.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("Sales Filters")

    selected_branches = st.sidebar.multiselect(
        "Select branch",
        options=sorted(daily_sales["branch"].dropna().unique()),
        default=sorted(daily_sales["branch"].dropna().unique())
    )

    selected_products = st.sidebar.multiselect(
        "Select product",
        options=sorted(daily_sales["item"].dropna().unique()),
        default=sorted(daily_sales["item"].dropna().unique())[:5]
    )

    if selected_branches:
        render_branch_legend(selected_branches, branch_color_map)

    date_range = st.sidebar.date_input(
        "Select date range",
        value=[
            daily_sales["operating_date"].min().date(),
            daily_sales["operating_date"].max().date()
        ]
    )

    filtered_data = daily_sales[
        (daily_sales["branch"].isin(selected_branches)) &
        (daily_sales["item"].isin(selected_products))
    ]

    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_data = filtered_data[
            (filtered_data["operating_date"] >= start_date) &
            (filtered_data["operating_date"] <= end_date)
        ]

    if filtered_data.empty:
        st.warning("No data available with the selected filters.")
        st.stop()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Units Sold", f"{filtered_data['quantity'].sum():,.0f}")
    col2.metric("Products Selected", filtered_data["item"].nunique())
    col3.metric("Branches Selected", filtered_data["branch"].nunique())
    col4.metric("Average Units per Record", f"{filtered_data['quantity'].mean():.2f}")

    st.subheader("Sales Visualizations")

    col1, col2 = st.columns(2)

    branch_sales = (
        filtered_data
        .groupby("branch")["quantity"]
        .sum()
        .reset_index()
        .sort_values("quantity", ascending=False)
    )

    top_branch = branch_sales.iloc[0]["branch"]

    fig_branch = px.bar(
        branch_sales,
        x="branch",
        y="quantity",
        color="branch",
        color_discrete_map=branch_color_map,
        title=f"{top_branch} leads total branch demand",
        text_auto=True
    )

    fig_branch.update_layout(showlegend=False)
    fig_branch.update_traces(
        textposition="outside",
        textfont_color="#2f2a26",
        marker_line_color="#FFFCF3",
        marker_line_width=0.5
    )
    fig_branch = apply_plot_theme(fig_branch)
    col1.plotly_chart(fig_branch, use_container_width=True)

    top_products_chart = (
        filtered_data
        .groupby("item")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    top_product = top_products_chart.iloc[0]["item"]
    top_products_chart = add_product_highlight(top_products_chart, "quantity")

    fig_products = px.bar(
        top_products_chart,
        x="quantity",
        y="item",
        color="product_highlight",
        orientation="h",
        color_discrete_map=product_color_map,
        title=f"{top_product} is the strongest product",
        text_auto=True
    )

    fig_products.update_layout(showlegend=False)
    fig_products.update_yaxes(categoryorder="total ascending")
    fig_products.update_traces(
        textposition="outside",
        textfont_color="#2f2a26",
        marker_line_color="#FFFCF3",
        marker_line_width=0.5
    )
    fig_products = apply_plot_theme(fig_products)
    col2.plotly_chart(fig_products, use_container_width=True)

    sales_time = (
        filtered_data
        .groupby(["operating_date", "branch"])["quantity"]
        .sum()
        .reset_index()
    )

    fig_time = px.line(
        sales_time,
        x="operating_date",
        y="quantity",
        color="branch",
        color_discrete_map=branch_color_map,
        title="Sales over time by branch",
        markers=False
    )

    fig_time.update_traces(line=dict(width=3))
    fig_time = apply_plot_theme(fig_time)
    st.plotly_chart(fig_time, use_container_width=True)

    weekday_sales = (
        filtered_data
        .groupby(["day_of_week", "day_name", "branch"])["quantity"]
        .sum()
        .reset_index()
        .sort_values("day_of_week")
    )

    fig_weekday = px.bar(
        weekday_sales,
        x="day_name",
        y="quantity",
        color="branch",
        color_discrete_map=branch_color_map,
        title="Sales by day of the week and branch",
        text_auto=True
    )

    fig_weekday.update_traces(
        textposition="outside",
        textfont_color="#2f2a26",
        marker_line_color="#FFFCF3",
        marker_line_width=0.5
    )
    fig_weekday = apply_plot_theme(fig_weekday)
    st.plotly_chart(fig_weekday, use_container_width=True)

    with st.expander("View Daily Sales Data"):
        st.dataframe(filtered_data, use_container_width=True)

# =====================================================
# PAGE 3: MODEL TRUST
# =====================================================

elif page == "3. Model Trust":

    st.header("Model Trust")

    st.markdown(
        """
        <div class="panem-note">
            This page translates model error into decision-friendly information. Lower error means the forecast is more reliable.
        </div>
        """,
        unsafe_allow_html=True
    )

    trust_table = model_results.copy()
    trust_table["Confidence"] = trust_table["MAPE"].apply(confidence_label)

    has_recent_baseline = "Recent_7_Day_MAPE" in trust_table.columns

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Model Error", f"{trust_table['MAPE'].mean():.2f}%")
    col2.metric("Average Historical Baseline Error", f"{trust_table['Baseline_MAPE'].mean():.2f}%")

    if has_recent_baseline:
        col3.metric("Average Recent 7-Day Error", f"{trust_table['Recent_7_Day_MAPE'].mean():.2f}%")
    else:
        col3.metric("Average Improvement", f"{trust_table['MAPE_Improvement_%'].mean():.2f}%")

    st.subheader("Model Error vs Baselines")

    comparison_columns = ["product", "MAPE", "Baseline_MAPE"]
    if "Recent_7_Day_MAPE" in trust_table.columns:
        comparison_columns.append("Recent_7_Day_MAPE")

    error_comparison = trust_table[comparison_columns].copy()
    error_comparison = error_comparison.rename(
        columns={
            "MAPE": "Model Engine",
            "Baseline_MAPE": "Historical Baseline",
            "Recent_7_Day_MAPE": "Recent 7-day Window"
        }
    )

    error_long = error_comparison.melt(
        id_vars="product",
        var_name="Method",
        value_name="Error %"
    )

    fig_error_compare = px.bar(
        error_long,
        x="product",
        y="Error %",
        color="Method",
        barmode="group",
        color_discrete_map={
            "Model Engine": "#5c432d",
            "Historical Baseline": "#c8ae87",
            "Recent 7-day Window": "#6f8f72"
        },
        title="Comparative Error Footprint (Lower Values Specify High Reliability)",
        text_auto=".1f"
    )

    fig_error_compare.add_hline(
        y=15.0, 
        line_dash="dash", 
        line_color="#b23b3b", 
        annotation_text="High Confidence Bound (15%)", 
        annotation_position="top right"
    )

    fig_error_compare.update_layout(
        xaxis=dict(title="Monitored Product Category"),
        yaxis=dict(title="Mean Absolute Percentage Error (MAPE)")
    )
    fig_error_compare.update_traces(
        textposition="outside",
        textfont=dict(size=10)
    )
    fig_error_compare = apply_plot_theme(fig_error_compare)

    st.plotly_chart(fig_error_compare, use_container_width=True)

    st.subheader("Error Difference by Product")

    trust_table["Error Difference"] = trust_table["Baseline_MAPE"] - trust_table["MAPE"]
    trust_table["Error Direction"] = trust_table["Error Difference"].apply(
        lambda x: "Model better" if x >= 0 else "Baseline better"
    )

    fig_error_diff = px.bar(
        trust_table,
        x="product",
        y="Error Difference",
        color="Error Direction",
        color_discrete_map={
            "Model better": positive_color,
            "Baseline better": negative_color
        },
        title="Positive values mean the model performs better than the historical baseline",
        text_auto=True
    )

    fig_error_diff.update_traces(
        textposition="outside",
        textfont_color="#2f2a26",
        marker_line_color="#FFFCF3",
        marker_line_width=0.5
    )
    fig_error_diff = apply_plot_theme(fig_error_diff)
    st.plotly_chart(fig_error_diff, use_container_width=True)

    st.subheader("Past Prediction Example")

    example_data = rolling_forecast.copy()
    example_data = example_data.dropna(subset=["date", "branch", "product", "actual", "predicted"])

    if example_data.empty:
        st.info("No past prediction examples are available.")
    else:
        example_data["day_name"] = example_data["date"].dt.day_name()

        example_col1, example_col2, example_col3 = st.columns(3)

        example_branch = example_col1.selectbox(
            "Select branch for example",
            options=sorted(example_data["branch"].dropna().unique()),
            key="example_branch"
        )

        product_options = sorted(
            example_data[example_data["branch"] == example_branch]["product"].dropna().unique()
        )

        example_product = example_col2.selectbox(
            "Select product for example",
            options=product_options,
            key="example_product"
        )

        filtered_example_data = example_data[
            (example_data["branch"] == example_branch) &
            (example_data["product"] == example_product)
        ].copy()

        filtered_example_data = filtered_example_data.sort_values("date", ascending=False)

        example_dates = (
            filtered_example_data["date"]
            .dt.strftime("%Y-%m-%d")
            .unique()
            .tolist()
        )

        example_date = example_col3.selectbox(
            "Select past prediction date",
            options=example_dates,
            key="example_date"
        )

        example_date = pd.to_datetime(example_date)

        example_row = filtered_example_data[
            filtered_example_data["date"] == example_date
        ].iloc[0]

        predicted_units = round(example_row["predicted"])
        actual_units = round(example_row["actual"])

        unit_error = predicted_units - actual_units
        absolute_unit_error = abs(unit_error)

        if unit_error > 0:
            error_text = f"the model overestimated demand by {absolute_unit_error} units"
            alert_class = "alert-negative"
        elif unit_error < 0:
            error_text = f"the model underestimated demand by {absolute_unit_error} units"
            alert_class = "alert-negative"
        else:
            error_text = "the model predicted the exact number of units sold"
            alert_class = "alert-positive"

        st.markdown(
            f"""
            <div class="{alert_class}">
                On <b>{example_row["day_name"]}</b>, for <b>{example_product}</b> at <b>{example_branch}</b>, 
                the model predicted <b>{predicted_units}</b> units, but the real sales were <b>{actual_units}</b> units. 
                Therefore, {error_text}.
            </div>
            """,
            unsafe_allow_html=True
        )

        example_chart = pd.DataFrame(
            {
                "Value": ["Predicted units", "Actual units"],
                "Units": [predicted_units, actual_units]
            }
        )

        fig_example = px.bar(
            example_chart,
            x="Value",
            y="Units",
            color="Value",
            color_discrete_map={
                "Predicted units": "#c8ae87",
                "Actual units": "#7a4f2f"
            },
            title="Predicted vs Actual Units for Selected Past Example",
            text_auto=True
        )

        fig_example.update_layout(showlegend=False)
        fig_example.update_traces(
            textposition="outside",
            textfont_color="#2f2a26",
            marker_line_color="#FFFCF3",
            marker_line_width=0.5
        )
        fig_example = apply_plot_theme(fig_example)
        st.plotly_chart(fig_example, use_container_width=True)

    display_columns = ["product", "MAPE", "Baseline_MAPE", "MAPE_Improvement_%", "Confidence"]
    if has_recent_baseline:
        display_columns.insert(3, "Recent_7_Day_MAPE")
        if "Recent_7_Day_MAPE_Improvement_%" in trust_table.columns:
            display_columns.insert(5, "Recent_7_Day_MAPE_Improvement_%")

    display_trust = trust_table[display_columns].copy()
    display_trust = display_trust.rename(
        columns={
            "product": "Product",
            "MAPE": "Model error %",
            "Baseline_MAPE": "Historical baseline error %",
            "Recent_7_Day_MAPE": "Recent 7-day baseline error %",
            "MAPE_Improvement_%": "Historical improvement %",
            "Recent_7_Day_MAPE_Improvement_%": "Recent baseline improvement %",
        }
    )

    with st.expander("View Model Trust Table"):
        st.dataframe(style_table(display_trust), use_container_width=True)

# =====================================================
# PAGE 4: UPDATE DATA
# =====================================================

elif page == "4. Update Data":

    st.header("Update Data")

    st.markdown(
        """
        <div class="panem-note">
            Use this page when a branch wants to add recent sales information. 
            The dashboard checks if the uploaded file overlaps with existing historical dates.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Instructions")
    st.markdown(
        """
        <div class="instruction-box">
            <b>1. Upload recent sales information.</b><br>
            The file should include at least these columns: <b>operating_date</b>, <b>branch</b>, <b>item</b>, and <b>quantity</b>.
        </div>
        <div class="instruction-box">
            <b>2. Check the date range.</b><br>
            Review whether the uploaded file contains new dates or dates that already exist in the historical data.
        </div>
        <div class="instruction-box">
            <b>3. Review overlap warnings.</b><br>
            If overlap appears, remove duplicates or decide whether the new rows should replace the old rows before retraining.
        </div>
        <div class="instruction-box">
            <b>4. Update the model datasource.</b><br>
            Use the uploaded file to regenerate <b>Panem_Dashboard_Datasource.xlsx</b> from the model notebook, then rerun Streamlit.
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Upload recent sales file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            new_data = pd.read_csv(uploaded_file)
        else:
            new_data = pd.read_excel(uploaded_file)

        new_data = clean_columns(new_data)

        st.subheader("Uploaded File Preview")
        st.dataframe(new_data.head(), use_container_width=True)

        required_update_cols = ["operating_date", "branch", "item", "quantity"]
        missing_update_cols = [col for col in required_update_cols if col not in new_data.columns]

        if missing_update_cols:
            st.error(f"Missing columns: {missing_update_cols}")
            st.stop()

        new_data["operating_date"] = pd.to_datetime(new_data["operating_date"], errors="coerce")
        new_data = new_data.dropna(subset=["operating_date"])

        old_min = daily_sales["operating_date"].min()
        old_max = daily_sales["operating_date"].max()
        new_min = new_data["operating_date"].min()
        new_max = new_data["operating_date"].max()

        col1, col2 = st.columns(2)
        col1.metric("Existing data starts", str(old_min.date()))
        col1.metric("Existing data ends", str(old_max.date()))
        col2.metric("Uploaded data starts", str(new_min.date()))
        col2.metric("Uploaded data ends", str(new_max.date()))

        overlap = new_data[
            (new_data["operating_date"] >= old_min) &
            (new_data["operating_date"] <= old_max)
        ]

        if not overlap.empty:
            st.markdown(
                """
                <div class="alert-negative">
                    Overlap detected. Some uploaded dates already exist in the historical data. 
                    Before retraining, remove duplicates or decide whether the new rows should replace old rows.
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write("Overlapping rows preview:")
            st.dataframe(overlap.head(), use_container_width=True)
        else:
            st.markdown(
                """
                <div class="alert-positive">
                    No date overlap detected. The uploaded data can be appended for model updating.
                </div>
                """,
                unsafe_allow_html=True
            )

# =====================================================
# PAGE 5: TECHNICAL DETAILS
# =====================================================

elif page == "5. Technical Details":

    st.header("Technical Details")

    st.markdown(
        """
        <div class="panem-note">
            Optional technical information for explaining how the model works.
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_product_error = st.selectbox(
        "Select product",
        options=sorted(weekly_errors["product"].dropna().unique())
    )

    err_filtered = weekly_errors[weekly_errors["product"] == selected_product_error].copy()

    col1, col2 = st.columns(2)

    mae_columns = ["mae", "historical_mae"]
    mape_columns = ["mape", "historical_mape"]

    if "recent_7_day_mae" in err_filtered.columns:
        mae_columns.append("recent_7_day_mae")

    if "recent_7_day_mape" in err_filtered.columns:
        mape_columns.append("recent_7_day_mape")

    fig_weekly_mae = px.line(
        err_filtered,
        x="week",
        y=mae_columns,
        markers=True,
        title=f"{selected_product_error}: Weekly MAE"
    )
    fig_weekly_mae.update_traces(line=dict(width=3))
    fig_weekly_mae = apply_plot_theme(fig_weekly_mae)
    col1.plotly_chart(fig_weekly_mae, use_container_width=True)

    fig_weekly_mape = px.line(
        err_filtered,
        x="week",
        y=mape_columns,
        markers=True,
        title=f"{selected_product_error}: Weekly MAPE"
    )
    fig_weekly_mape.update_traces(line=dict(width=3))
    fig_weekly_mape = apply_plot_theme(fig_weekly_mape)
    col2.plotly_chart(fig_weekly_mape, use_container_width=True)

    if not feature_importance.empty:
        st.subheader("Feature Importance")

        selected_product_feature = st.selectbox(
            "Select product for feature importance",
            options=sorted(feature_importance["product"].dropna().unique())
        )

        feature_filtered = (
            feature_importance[feature_importance["product"] == selected_product_feature]
            .sort_values("importance", ascending=False)
            .head(10)
        )

        fig_features = px.bar(
            feature_filtered,
            x="importance",
            y="feature",
            orientation="h",
            title=f"{selected_product_feature}: Top Features"
        )

        fig_features.update_traces(
            marker_color=highlight_color,
            textposition="outside",
            textfont_color="#2f2a26",
            marker_line_color="#FFFCF3",
            marker_line_width=0.5
        )
        fig_features = apply_plot_theme(fig_features)
        st.plotly_chart(fig_features, use_container_width=True)

    with st.expander("View Model Results"):
        st.dataframe(model_results, use_container_width=True)

    with st.expander("View Weekly Errors"):
        st.dataframe(weekly_errors, use_container_width=True)

    with st.expander("View Feature Importance"):
        st.dataframe(feature_importance, use_container_width=True)