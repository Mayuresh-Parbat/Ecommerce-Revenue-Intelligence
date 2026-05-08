import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="E-commerce Revenue Intelligence",
    layout="wide",
    page_icon="📊"
)

# LOAD DATA
df = pd.read_csv("data/processed/cleaned_data.csv")

# DATE CONVERSION
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# SIDEBAR
st.sidebar.title("🔍 Dashboard Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    sorted(df['Country'].dropna().unique())
)

# FILTER DATA
filtered_df = df[df['Country'] == selected_country]

# KPIs
total_revenue = filtered_df['Revenue'].sum()
total_orders = filtered_df['InvoiceNo'].nunique()
total_customers = filtered_df['CustomerID'].nunique()
avg_order_value = total_revenue / total_orders

# TITLE
st.title("📊 E-commerce Revenue Intelligence Dashboard")

st.markdown("""
Professional analytics dashboard for monitoring sales,
customer intelligence, and revenue performance.
""")

st.divider()

# KPI ROW
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Revenue",
        f"${total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "🛒 Orders",
        total_orders
    )

with col3:
    st.metric(
        "👥 Customers",
        total_customers
    )

with col4:
    st.metric(
        "📦 Avg Order Value",
        f"${avg_order_value:,.2f}"
    )

st.divider()

# AI INSIGHTS
st.subheader("🤖 AI Business Insights")

if total_revenue > 1000000:
    st.success(
        "Strong revenue performance detected with healthy customer purchasing activity."
    )

if total_customers > 1000:
    st.info(
        "Customer acquisition is performing well with scalable growth potential."
    )

if avg_order_value > 400:
    st.warning(
        "High average order value indicates premium purchasing behavior."
    )

st.divider()

# TOP COUNTRIES
st.subheader("🌍 Top 10 Countries by Revenue")

country_revenue = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_country = px.bar(
    country_revenue,
    x="Country",
    y="Revenue",
    color="Revenue",
    text_auto=".2s",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig_country, use_container_width=True)

# MONTHLY REVENUE
st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = (
    filtered_df.groupby(
        filtered_df['InvoiceDate'].dt.to_period('M')
    )['Revenue']
    .sum()
    .reset_index()
)

monthly_revenue['InvoiceDate'] = monthly_revenue['InvoiceDate'].astype(str)

fig_monthly = px.line(
    monthly_revenue,
    x="InvoiceDate",
    y="Revenue",
    markers=True,
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig_monthly, use_container_width=True)

# TOP CUSTOMERS
st.subheader("🏆 Top Customers")

top_customers = (
    filtered_df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_customers = px.bar(
    top_customers,
    x="CustomerID",
    y="Revenue",
    color="Revenue",
    template="plotly_dark",
    text_auto=".2s",
    height=500
)

st.plotly_chart(fig_customers, use_container_width=True)

# CUSTOMER SEGMENTS
st.subheader("🧠 Customer Segmentation")

segment_data = (
    filtered_df.groupby('CustomerID')
    .agg({
        'InvoiceNo': 'count',
        'Revenue': 'sum'
    })
    .reset_index()
)

segment_data.columns = ['CustomerID', 'Frequency', 'Monetary']

fig_segment = px.scatter(
    segment_data,
    x="Frequency",
    y="Monetary",
    size="Monetary",
    color="Monetary",
    hover_data=["CustomerID"],
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig_segment, use_container_width=True)

# DOWNLOAD BUTTON
st.subheader("📥 Export Data")

st.download_button(
    label="Download Clean Dataset",
    data=filtered_df.to_csv(index=False),
    file_name="cleaned_data.csv",
    mime="text/csv"
)

# DATA PREVIEW
st.subheader("📄 Data Preview")

st.dataframe(filtered_df.head(20))

st.success("Dashboard running successfully 🚀")