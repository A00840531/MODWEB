import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="Panem Demand Dashboard",
    layout="wide"
)

# =====================================================
# CREAM + MONOSPACE STYLE THEME
# =====================================================

st.markdown(
    """
    <style>
    /* Whole app */
    .stApp {
    background-color: #fffaf0;
    color: #2f2a26;
    font-family: "Courier New", monospace;
    }

    html, body, [class*="css"] {
        font-family: "Courier New", monospace;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
    background-color: #f7ecd8;
    border-right: 1px solid #e2cba9;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #3a3028 !important;
        font-family: "Courier New", monospace;
    }

    /* Multiselect selected tags */
    [data-baseweb="tag"] {
        background-color: #e6d3b3 !important;
        color: #3a3028 !important;
        border-radius: 6px !important;
        border: 1px solid #c7a982 !important;
        font-family: "Courier New", monospace;
    }

    [data-baseweb="tag"] svg {
        color: #3a3028 !important;
        fill: #3a3028 !important;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #fff8ec !important;
        border-color: #d8c3a5 !important;
        color: #3a3028 !important;
    }

    /* Hero title */
    .panem-hero {
        background: linear-gradient(90deg, #b79a73 0%, #d8c3a5 100%);
        padding: 28px 34px;
        border-radius: 6px;
        margin-bottom: 18px;
        border-left: 10px solid #5c432d;
    }

    .panem-title {
        color: #fffaf0;
        font-size: 72px;
        font-weight: 900;
        margin: 0;
        letter-spacing: 4px;
        font-family: "Courier New", monospace;
    }

    .panem-subtitle {
        font-size: 20px;
        color: #3a3028;
        margin-top: 12px;
        margin-bottom: 18px;
        max-width: 1050px;
        line-height: 1.45;
        font-family: "Courier New", monospace;
    }

    .panem-note {
        background-color: #fff8ec;
        border-left: 6px solid #8b6f47;
        padding: 14px 18px;
        border-radius: 4px;
        margin-bottom: 28px;
        font-size: 16px;
    }

    /* Section headers */
    h1, h2, h3 {
        color: #2f2a26 !important;
        font-family: "Courier New", monospace !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #fff8ec;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #d8c3a5;
        box-shadow: 0px 2px 8px rgba(92, 67, 45, 0.08);
    }

    /* Expander */
    div[data-testid="stExpander"] {
        background-color: #fff8ec;
        border-radius: 10px;
        border: 1px solid #d8c3a5;
    }

    /* Divider-like spacing */
    .block-container {
        padding-top: 2rem;
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
        paper_bgcolor="#fffaf0",
        plot_bgcolor="#fffaf0",
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
            bgcolor="rgba(255,250,240,0)",
            font=dict(color="#2f2a26")
        ),
        margin=dict(l=40, r=30, t=70, b=40)
    )
    return fig

# =====================================================
# LOAD EXCEL DATASOURCE (ROBUST RELATIVE PATH FIX)
# =====================================================

# Get the exact folder where this pandash.py script resides
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
excel_file = os.path.join(BASE_DIR, "Panem_Dashboard_Datasource.xlsx")

if not os.path.exists(excel_file):
    st.error(
        f"Excel file not found at: {excel_file}. Please place "
        "'Panem_Dashboard_Datasource.xlsx' in the exact same directory as your script."
    )
    st.stop()

daily_sales = clean_columns(
    pd.read_excel(excel_file, sheet_name="Daily_Sales")
)

model_results = clean_columns(
    pd.read_excel(excel_file, sheet_name="Model_Results")
)

weekly_errors = clean_columns(
    pd.read_excel(excel_file, sheet_name="Weekly_Errors")
)

rolling_forecast = clean_columns(
    pd.read_excel(excel_file, sheet_name="Rolling_Forecast")
)

try:
    feature_importance = clean_columns(
        pd.read_excel(excel_file, sheet_name="Feature_Importance")
    )
except:
    feature_importance = pd.DataFrame()


# =====================================================
# PREPARE DATA
# =====================================================

daily_sales = format_date_column(daily_sales, "operating_date")
rolling_forecast = format_date_column(rolling_forecast, "date")

daily_sales = daily_sales.dropna(subset=["operating_date"])
rolling_forecast = rolling_forecast.dropna(subset=["date"])

# Clean names
daily_sales["branch"] = daily_sales["branch"].apply(clean_name)
daily_sales["item"] = daily_sales["item"].apply(clean_name)

model_results["product"] = model_results["product"].apply(clean_name)

weekly_errors["product"] = weekly_errors["product"].apply(clean_name)

rolling_forecast["product"] = rolling_forecast["product"].apply(clean_name)
rolling_forecast["branch"] = rolling_forecast["branch"].apply(clean_name)

if not feature_importance.empty:
    feature_importance["product"] = feature_importance["product"].apply(clean_name)

# Day names
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
# TITLE AND NAVIGATION
# =====================================================

st.markdown(
    """
    <div class="panem-hero">
        <h1 class="panem-title">PANEM</h1>
    </div>

    <div class="panem-note">
        The visualizations use muted cream tones, while the strongest or most relevant values are highlighted to make the main insight easier to identify.
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select page",
    [
        "1. Historical Sales",
        "2. Model Comparison",
        "3. Weekly Errors",
        "4. Feature Importance",
        "5. Forecast Predictions"
    ]
)


# =====================================================
# PAGE 1: HISTORICAL SALES
# =====================================================

if page == "1. Historical Sales":

    st.header("Historical Sales Overview")

    st.markdown(
        """
        <div class="panem-note">
            This page shows where Panem sells the most, which products dominate demand, 
            and when the strongest sales peaks happen. The darkest bars highlight the highest values.
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

    # -----------------------------
    # KPIs
    # -----------------------------

    st.subheader("Main Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Units Sold", f"{filtered_data['quantity'].sum():,.0f}")
    col2.metric("Products Selected", filtered_data["item"].nunique())
    col3.metric("Branches Selected", filtered_data["branch"].nunique())
    col4.metric("Average Units per Record", f"{filtered_data['quantity'].mean():.2f}")

    # -----------------------------
    # Colors
    # -----------------------------

    base_color = "#d8c3a5"
    soft_color = "#ead8bd"
    highlight_color = "#5c432d"
    line_color = "#8b6f47"

    st.subheader("Sales Visualizations")

    col1, col2 = st.columns(2)

    # -----------------------------
    # Branch sales
    # -----------------------------

    branch_sales = (
        filtered_data
        .groupby("branch")["quantity"]
        .sum()
        .reset_index()
        .sort_values("quantity", ascending=False)
    )

    top_branch = branch_sales.iloc[0]["branch"]
    max_branch_value = branch_sales.iloc[0]["quantity"]

    branch_sales["highlight"] = branch_sales["branch"].apply(
        lambda x: "Highest branch" if x == top_branch else "Other branches"
    )

    fig_branch = px.bar(
        branch_sales,
        x="branch",
        y="quantity",
        color="highlight",
        color_discrete_map={
            "Highest branch": highlight_color,
            "Other branches": base_color
        },
        title=f"{top_branch} leads total branch demand",
        text_auto=True
    )

    fig_branch.update_layout(showlegend=False)
    fig_branch.update_traces(
        textfont_color="white",
        marker_line_color="#fffaf0",
        marker_line_width=0.5
    )

    fig_branch = apply_plot_theme(fig_branch)

    col1.plotly_chart(fig_branch, use_container_width=True)

    # -----------------------------
    # Top products
    # -----------------------------

    top_products_chart = (
        filtered_data
        .groupby("item")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    top_product = top_products_chart.iloc[0]["item"]

    top_products_chart["highlight"] = top_products_chart["item"].apply(
        lambda x: "Top product" if x == top_product else "Other products"
    )

    fig_products = px.bar(
        top_products_chart,
        x="quantity",
        y="item",
        color="highlight",
        orientation="h",
        color_discrete_map={
            "Top product": highlight_color,
            "Other products": base_color
        },
        title=f"{top_product} is the strongest product",
        text_auto=True
    )

    fig_products.update_layout(showlegend=False)
    fig_products.update_yaxes(categoryorder="total ascending")
    fig_products.update_traces(
        textfont_color="white",
        marker_line_color="#fffaf0",
        marker_line_width=0.5
    )

    fig_products = apply_plot_theme(fig_products)

    col2.plotly_chart(fig_products, use_container_width=True)

    # -----------------------------
    # Sales over time
    # -----------------------------

    sales_time = (
        filtered_data
        .groupby("operating_date")["quantity"]
        .sum()
        .reset_index()
    )

    peak_row = sales_time.loc[sales_time["quantity"].idxmax()]

    fig_time = px.line(
        sales_time,
        x="operating_date",
        y="quantity",
        title="Sales over time with the strongest peak highlighted",
        markers=False
    )

    fig_time.update_traces(
        line=dict(color=line_color, width=3)
    )

    fig_time.add_scatter(
        x=[peak_row["operating_date"]],
        y=[peak_row["quantity"]],
        mode="markers+text",
        marker=dict(size=15, color=highlight_color),
        text=[f"Peak: {peak_row['quantity']:.0f}"],
        textposition="top center",
        name="Peak"
    )

    fig_time = apply_plot_theme(fig_time)

    st.plotly_chart(fig_time, use_container_width=True)

    # -----------------------------
    # Weekday sales
    # -----------------------------

    weekday_sales = (
        filtered_data
        .groupby(["day_of_week", "day_name"])["quantity"]
        .sum()
        .reset_index()
        .sort_values("day_of_week")
    )

    top_weekday = weekday_sales.loc[weekday_sales["quantity"].idxmax(), "day_name"]

    weekday_sales["highlight"] = weekday_sales["day_name"].apply(
        lambda x: "Strongest weekday" if x == top_weekday else "Other weekdays"
    )

    fig_weekday = px.bar(
        weekday_sales,
        x="day_name",
        y="quantity",
        color="highlight",
        color_discrete_map={
            "Strongest weekday": highlight_color,
            "Other weekdays": soft_color
        },
        title=f"{top_weekday} is the strongest sales day",
        text_auto=True
    )

    fig_weekday.update_layout(showlegend=False)
    fig_weekday.update_traces(
        textfont_color="white",
        marker_line_color="#fffaf0",
        marker_line_width=0.5
    )

    fig_weekday = apply_plot_theme(fig_weekday)

    st.plotly_chart(fig_weekday, use_container_width=True)

    with st.expander("View Daily Sales Data"):
        st.dataframe(filtered_data)




# =====================================================
# PAGE 2: MODEL COMPARISON
# =====================================================

elif page == "2. Model Comparison":

    st.header("Model Comparison")

    st.write(
        "This page uses the Model_Results sheet. It compares the Gradient Boosting model against the historical baseline."
    )

    with st.expander("View Model Results Table"):
        st.dataframe(model_results)

    st.subheader("Model Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average Model MAE",
        f"{model_results['MAE'].mean():.2f}"
    )

    col2.metric(
        "Average Baseline MAE",
        f"{model_results['Baseline_MAE'].mean():.2f}"
    )

    col3.metric(
        "Average MAE Improvement",
        f"{model_results['MAE_Improvement_%'].mean():.2f}%"
    )

    col4.metric(
        "Average R²",
        f"{model_results['R2'].mean():.2f}"
    )

    st.subheader("Model vs Historical Baseline")

    col1, col2 = st.columns(2)

    fig_mae = px.bar(
        model_results,
        x="product",
        y=["Baseline_MAE", "MAE"],
        barmode="group",
        title="MAE Comparison: Historical Baseline vs Gradient Boosting"
    )
    fig_mae = apply_plot_theme(fig_mae)

    col1.plotly_chart(fig_mae, use_container_width=True)

    fig_mape = px.bar(
        model_results,
        x="product",
        y=["Baseline_MAPE", "MAPE"],
        barmode="group",
        title="MAPE Comparison: Historical Baseline vs Gradient Boosting"
    )
    fig_mape = apply_plot_theme(fig_mape)

    col2.plotly_chart(fig_mape, use_container_width=True)

    fig_r2 = px.bar(
        model_results,
        x="product",
        y="R2",
        title="R² Score by Product",
        text_auto=True
    )
    fig_r2 = apply_plot_theme(fig_r2)

    st.plotly_chart(fig_r2, use_container_width=True)

    st.subheader("Interpretation")

    st.write(
        "Lower MAE and MAPE indicate better predictive performance. "
        "This page shows whether the Gradient Boosting model predicts demand more accurately than the historical baseline."
    )


# =====================================================
# PAGE 3: WEEKLY ERRORS
# =====================================================

elif page == "3. Weekly Errors":

    st.header("Weekly Errors")

    st.write(
        "This page uses the Weekly_Errors sheet. It shows how the model error changes week by week."
    )

    selected_product_error = st.selectbox(
        "Select product",
        options=sorted(weekly_errors["product"].dropna().unique())
    )

    err_filtered = weekly_errors[
        weekly_errors["product"] == selected_product_error
    ].copy()

    st.subheader("Weekly Error Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Average Weekly MAE", f"{err_filtered['mae'].mean():.2f}")
    col2.metric("Average Historical MAE", f"{err_filtered['historical_mae'].mean():.2f}")
    col3.metric("Average Weekly MAPE", f"{err_filtered['mape'].mean():.2f}%")
    col4.metric("Average Historical MAPE", f"{err_filtered['historical_mape'].mean():.2f}%")

    st.subheader("Weekly Error Trends")

    col1, col2 = st.columns(2)

    fig_weekly_mae = px.line(
        err_filtered,
        x="week",
        y=[
            "mae",
            "historical_mae",
            "mae_cumulative",
            "historical_mae_cumulative"
        ],
        markers=True,
        title=f"{selected_product_error}: Weekly MAE"
    )
    fig_weekly_mae = apply_plot_theme(fig_weekly_mae)

    col1.plotly_chart(fig_weekly_mae, use_container_width=True)

    fig_weekly_mape = px.line(
        err_filtered,
        x="week",
        y=[
            "mape",
            "historical_mape",
            "mape_cumulative",
            "historical_mape_cumulative"
        ],
        markers=True,
        title=f"{selected_product_error}: Weekly MAPE"
    )
    fig_weekly_mape = apply_plot_theme(fig_weekly_mape)

    col2.plotly_chart(fig_weekly_mape, use_container_width=True)

    with st.expander("View Weekly Errors Table"):
        st.dataframe(err_filtered)

    st.subheader("Interpretation")

    st.write(
        "This page helps identify whether the model performs consistently over time. "
        "If the Gradient Boosting error lines are below the historical baseline lines, the model is performing better."
    )


# =====================================================
# PAGE 4: FEATURE IMPORTANCE
# =====================================================

elif page == "4. Feature Importance":

    st.header("Feature Importance")

    st.write(
        "This page uses the Feature_Importance sheet. It shows which variables had the strongest influence on the model predictions."
    )

    if feature_importance.empty:
        st.warning("Feature_Importance sheet was not found in the Excel file.")
        st.stop()

    selected_product_feature = st.selectbox(
        "Select product",
        options=sorted(feature_importance["product"].dropna().unique())
    )

    feature_filtered = (
        feature_importance[
            feature_importance["product"] == selected_product_feature
        ]
        .sort_values("importance", ascending=False)
        .head(10)
    )

    st.subheader("Top Influential Features")

    fig_features = px.bar(
        feature_filtered,
        x="importance",
        y="feature",
        orientation="h",
        title=f"{selected_product_feature}: Top Features"
    )
    fig_features = apply_plot_theme(fig_features)

    st.plotly_chart(fig_features, use_container_width=True)

    with st.expander("View Feature Importance Table"):
        st.dataframe(feature_filtered)

    st.subheader("Interpretation")

    st.write(
        "Feature importance shows which inputs the model used most to make its predictions. "
        "For example, lag and rolling variables usually indicate that recent demand patterns are important for forecasting future sales."
    )


# =====================================================
# PAGE 5: FORECAST PREDICTIONS
# =====================================================

elif page == "5. Forecast Predictions":

    st.header("Forecast Predictions")

    st.write(
        "This page uses the Rolling_Forecast sheet. It presents actual demand, model prediction, historical baseline, and business forecast indicators."
    )

    st.subheader("Options")

    col1, col2, col3, col4 = st.columns(4)

    selected_branch = col1.selectbox(
        "Branch",
        options=sorted(rolling_forecast["branch"].dropna().unique())
    )

    selected_product = col2.selectbox(
        "Product",
        options=sorted(rolling_forecast["product"].dropna().unique())
    )

    forecast_days = col3.selectbox(
        "Forecast window",
        options=[7, 14, 30],
        index=0
    )

    unit_price = col4.number_input(
        "Unit price",
        min_value=1.0,
        value=50.0,
        step=1.0
    )

    cost_of_goods = st.number_input(
        "Estimated cost of goods per unit",
        min_value=1.0,
        value=25.0,
        step=1.0
    )

    forecast_filtered = rolling_forecast[
        (rolling_forecast["branch"] == selected_branch) &
        (rolling_forecast["product"] == selected_product)
    ].copy()

    forecast_filtered = forecast_filtered.sort_values("date")

    if forecast_filtered.empty:
        st.warning("No forecast data available for this branch and product.")
        st.stop()

    forecast_window = forecast_filtered.tail(forecast_days).copy()

    forecast_window["forecasted_revenue"] = (
        forecast_window["predicted"] * unit_price
    )

    forecast_window["estimated_cog"] = (
        forecast_window["predicted"] * cost_of_goods
    )

    forecast_window["gross_profit"] = (
        forecast_window["forecasted_revenue"] -
        forecast_window["estimated_cog"]
    )

    st.subheader(f"Forecast Window: Latest {forecast_days} Prediction Days")

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        "Forecasted Revenue",
        f"${forecast_window['forecasted_revenue'].sum():,.2f}"
    )

    kpi2.metric(
        "Estimated Cost of Goods",
        f"${forecast_window['estimated_cog'].sum():,.2f}"
    )

    kpi3.metric(
        "Gross Profit",
        f"${forecast_window['gross_profit'].sum():,.2f}"
    )

    kpi4, kpi5, kpi6 = st.columns(3)

    kpi4.metric(
        "Forecasted Units",
        f"{forecast_window['predicted'].sum():,.0f}"
    )

    kpi5.metric(
        "Average Absolute Error",
        f"{forecast_window['absolute_error'].mean():.2f}"
    )

    kpi6.metric(
        "Average Percentage Error",
        f"{forecast_window['percentage_error'].mean():.2f}%"
    )

    st.subheader("Actual vs Model Forecast vs Historical Baseline")

    line_data = forecast_window[
        [
            "date",
            "actual",
            "predicted",
            "historical_baseline"
        ]
    ].copy()

    line_data = line_data.melt(
        id_vars="date",
        value_vars=[
            "actual",
            "predicted",
            "historical_baseline"
        ],
        var_name="series",
        value_name="quantity"
    )

    line_data["series"] = line_data["series"].replace({
        "actual": "Actual Sales",
        "predicted": "Model Forecast",
        "historical_baseline": "Historical Baseline"
    })

    fig_forecast = px.line(
        line_data,
        x="date",
        y="quantity",
        color="series",
        markers=True,
        title=f"{selected_product} — {selected_branch}: Forecast Comparison"
    )
    fig_forecast = apply_plot_theme(fig_forecast)

    st.plotly_chart(fig_forecast, use_container_width=True)

    st.subheader("Forecast Breakdown")

    col1, col2 = st.columns(2)

    fig_daily_forecast = px.bar(
        forecast_window,
        x="date",
        y="predicted",
        title="Predicted Units by Day",
        text_auto=True
    )
    fig_daily_forecast = apply_plot_theme(fig_daily_forecast)

    col1.plotly_chart(fig_daily_forecast, use_container_width=True)

    fig_error = px.bar(
        forecast_window,
        x="date",
        y="absolute_error",
        title="Absolute Error by Day",
        text_auto=True
    )
    fig_error = apply_plot_theme(fig_error)

    col2.plotly_chart(fig_error, use_container_width=True)

    st.subheader("Forecast Financial Table")

    display_table = forecast_window[
        [
            "date",
            "product",
            "branch",
            "actual",
            "predicted",
            "historical_baseline",
            "absolute_error",
            "percentage_error",
            "forecasted_revenue",
            "estimated_cog",
            "gross_profit"
        ]
    ].copy()

    display_table["date"] = display_table["date"].dt.date

    st.dataframe(display_table)

    st.subheader("Interpretation")

    st.write(
        "The line chart compares actual sales, model forecast, and the historical baseline. "
        "The KPI cards translate the forecasted units into estimated revenue, cost of goods, and gross profit."
    )