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

# CONVERT DATE
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# KPIs
total_revenue = df['Revenue'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()

# TITLE
st.title("📊 E-commerce Revenue Intelligence Dashboard")

st.markdown(
    "Interactive analytics dashboard for revenue, customers, and sales insights."
)

st.divider()

# KPI CARDS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Revenue", f"${total_revenue:,.0f}")

with col2:
    st.metric("🛒 Orders", total_orders)

with col3:
    st.metric("👥 Customers", total_customers)

st.divider()

# TOP COUNTRIES
st.subheader("🌍 Top Countries by Revenue")

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
    height=450,
    text_auto='.2s'
)

st.plotly_chart(fig_country, use_container_width=True)

# MONTHLY REVENUE
st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = (
    df.groupby(df['InvoiceDate'].dt.to_period('M'))['Revenue']
    .sum()
    .reset_index()
)

monthly_revenue['InvoiceDate'] = monthly_revenue['InvoiceDate'].astype(str)

fig_monthly = px.line(
    monthly_revenue,
    x="InvoiceDate",
    y="Revenue",
    markers=True,
    height=450
)

st.plotly_chart(fig_monthly, use_container_width=True)

# TOP CUSTOMERS
st.subheader("🏆 Top Customers")

top_customers = (
    df.groupby("CustomerID")["Revenue"]
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
    height=450,
    text_auto='.2s'
)

st.plotly_chart(fig_customers, use_container_width=True)

# COUNTRY FILTER
st.sidebar.header("🔍 Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    df['Country'].unique()
)

filtered_df = df[df['Country'] == selected_country]

st.subheader(f"📦 Orders from {selected_country}")

st.dataframe(filtered_df.head(20))

st.success("AI-powered dashboard running successfully 🚀")