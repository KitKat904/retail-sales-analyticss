import streamlit as st
import plotly.express as px
import pandas as pd
from analysis import load_data, clean_data, analyze_data, product_sales, store_sales, ml_forecast
from database import store_data

# Page setup
st.set_page_config(page_title="Retail Dashboard", layout="wide")

# Title
st.title("🛍️ Retail Sales Analytics & Demand Forecasting System")
st.markdown("### 📊 Analyze past sales and predict future demand")
st.markdown("---")

# Load data
data = load_data()
data = clean_data(data)

# Store in database
store_data(data)

# Sidebar filters
st.sidebar.header("🔎 Filters")

product = st.sidebar.selectbox("Select Product", data['Product'].unique())
store = st.sidebar.selectbox("Select Store", data['Store'].unique())

filtered_data = data[
    (data['Product'] == product) &
    (data['Store'] == store)
]

# Analysis
total, monthly = analyze_data(data)

# Metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("💰 Total Sales", total)

with col2:
    st.metric("📦 Selected Product", product)

st.markdown("---")

# Charts
col3, col4 = st.columns(2)

with col3:
    st.subheader("📈 Monthly Sales Trend")
    fig1 = px.line(monthly, title="Sales Over Time")
    st.plotly_chart(fig1, use_container_width=True)

with col4:
    st.subheader("📊 Product Sales")
    fig2 = px.bar(product_sales(data), title="Product Distribution")
    st.plotly_chart(fig2, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    st.subheader("🏬 Store Distribution")
    fig3 = px.pie(
        values=store_sales(data).values,
        names=store_sales(data).index,
        title="Store Share"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col6:
    st.subheader("🔮 ML Forecast")

    forecast_values = ml_forecast(monthly)

    future_months = ["Next1", "Next2", "Next3"]

    forecast_df = pd.DataFrame({
        "Month": future_months,
        "Forecast Sales": forecast_values
    })

    st.line_chart(forecast_df.set_index("Month"))

st.markdown("---")

# Insights
st.markdown("## 🧠 Key Insights")

best_product = product_sales(data).idxmax()
best_store = store_sales(data).idxmax()

col7, col8 = st.columns(2)

with col7:
    st.success(f"🏆 Best Product: {best_product}")

with col8:
    st.success(f"🏬 Best Store: {best_store}")

st.markdown("---")

# Filtered data
st.subheader("📋 Filtered Data")

if filtered_data.empty:
    st.warning("No data available ❗")
else:
    st.dataframe(filtered_data)