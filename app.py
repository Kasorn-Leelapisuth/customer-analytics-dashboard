# Import plotly express for responsive charts
import plotly.express as px
# Import streamlit to construct the web dashboard
import streamlit as st
# Import our SQL analytics functions
from analytics_engine import (
    get_monthly_revenue,
    get_repeat_customer_rate,
    get_summary_kpis,
    get_top_products_by_revenue,
    load_csv_to_db,
)

# Make sure SQLite table is loaded from CSV
load_csv_to_db()

# Browser window configuration
st.set_page_config(
    page_title="Executive Sales & Customer Dashboard",
    layout="wide",
)

st.title("Executive E-Commerce & Customer Retention Dashboard")
st.caption("Powered by SQLite & SQL Window Functions")

# Fetch KPI metrics from SQL
kpis = get_summary_kpis()
repeat_data = get_repeat_customer_rate()

# Metric Cards Row
col1, col2, col3, col4 = st.columns(4)
total_rev = kpis["total_revenue"].iloc[0]
avg_order = kpis["average_order_value"].iloc[0]
total_orders = kpis["total_orders"].iloc[0]
repeat_rate = repeat_data["repeat_rate_pct"].iloc[0]

col1.metric("Total Revenue", f"${total_rev:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Avg Order Value (AOV)", f"${avg_order:,.2f}")
col4.metric("Repeat Customer Rate", f"{repeat_rate}%")

st.markdown("---")

# Visualizations Row: Revenue Trend & Top Products
row1_left, row1_right = st.columns([1, 1])

with row1_left:
    st.subheader("Monthly Revenue Growth")
    monthly_df = get_monthly_revenue()
    fig_revenue = px.line(
        monthly_df,
        x="order_month",
        y="monthly_revenue",
        markers=True,
        title="Monthly Completed Revenue ($)",
        labels={
            "order_month": "Month",
            "monthly_revenue": "Revenue ($AUD)",
        },
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with row1_right:
    st.subheader("Top Revenue Generators")
    products_df = get_top_products_by_revenue()
    fig_products = px.bar(
        products_df,
        x="product_revenue",
        y="product_name",
        orientation="h",
        color="category",
        title="Product Revenue Breakdown",
        labels={
            "product_revenue": "Revenue ($AUD)",
            "product_name": "Product",
        },
    )
    # Invert y-axis so rank 1 is on top
    fig_products.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_products, use_container_width=True)

# Data Table Exploration Section
st.subheader("SQL Ranked Product Performance Table")
st.dataframe(products_df, use_container_width=True)