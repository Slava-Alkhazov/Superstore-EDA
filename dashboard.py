import streamlit as st
st.set_page_config(layout="wide", page_title="Superstore Sales Dashboard")

import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    """Load and preprocess the Superstore dataset."""
    url = (
        "https://gist.githubusercontent.com/nnbphuong/"
        "38db511db14542f3ba9ef16e69d3814c/raw/Superstore.csv"
    )
    df = pd.read_csv(url, parse_dates=['Order Date', 'Ship Date'])
    df = df.dropna(subset=['Postal Code'])
    df['YearMonth'] = df['Order Date'].dt.to_period('M').astype(str)
    return df

# 1) Load data
df = load_data()

# 2) KPI block
total_sales  = df['Sales'].sum()
total_orders = df.shape[0]
avg_profit   = df['Profit'].mean()

st.title("🛒 Superstore Sales Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales",     f"${total_sales:,.0f}")
col2.metric("Orders Count",    f"{total_orders}")
col3.metric("Average Profit",  f"${avg_profit:,.2f}")

st.markdown("---")

# 3) Monthly sales line chart
monthly = df.groupby('YearMonth')['Sales'].sum().reset_index()
sel_month = st.selectbox("Select Month", monthly['YearMonth'].tolist())
month_val = monthly.loc[monthly.YearMonth==sel_month, 'Sales'].values[0]
st.write(f"**Sales in {sel_month}:** ${month_val:,.2f}")

fig1 = px.line(
    monthly,
    x='YearMonth',
    y='Sales',
    title='Monthly Sales Over Time',
    labels={'YearMonth':'Year-Month','Sales':'Sales'}
)
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# 4) Total Sales by Category
st.subheader("Total Sales by Category")
cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
fig2 = px.bar(
    cat_sales,
    x='Category',
    y='Sales',
    title='Total Sales by Category',
    labels={'Category':'Category','Sales':'Sales'}
)
st.plotly_chart(fig2, use_container_width=True)

# 5) Total Sales by Region
st.subheader("Total Sales by Region")
region_sales = df.groupby('Region')['Sales'].sum().reset_index()
fig3 = px.bar(
    region_sales,
    x='Region',
    y='Sales',
    title='Total Sales by Region',
    labels={'Region':'Region','Sales':'Sales'}
)
st.plotly_chart(fig3, use_container_width=True)

# 6) Top 5 Products by Sales
st.subheader("Top 5 Products by Sales")
top_products = (
    df.groupby('Product Name')['Sales']
      .sum()
      .reset_index()
      .sort_values('Sales', ascending=False)
      .head(5)
)
fig4 = px.bar(
    top_products,
    x='Product Name',
    y='Sales',
    title='Top 5 Products',
    labels={'Product Name':'Product','Sales':'Sales'}
)
fig4.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig4, use_container_width=True)

# 7) Total Sales by Sub-Category
st.subheader("Total Sales by Sub-Category")
subcat_sales = (
    df.groupby('Sub-Category')['Sales']
      .sum()
      .reset_index()
      .sort_values('Sales', ascending=False)
)
fig5 = px.bar(
    subcat_sales,
    x='Sales',
    y='Sub-Category',
    orientation='h',
    title='Sales by Sub-Category',
    labels={'Sub-Category':'Sub-Category','Sales':'Sales'}
)
fig5.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig5, use_container_width=True)

# 8) Sales Distribution by Segment
st.subheader("Sales Distribution by Segment")
seg_sales = df.groupby('Segment')['Sales'].sum().reset_index()
fig6 = px.pie(
    seg_sales,
    names='Segment',
    values='Sales',
    title='Sales Share by Segment'
)
st.plotly_chart(fig6, use_container_width=True)

# 9) Sales vs Profit scatter
st.subheader("Sales vs Profit by Product")
fig7 = px.scatter(
    df,
    x='Sales',
    y='Profit',
    color='Category',
    size='Quantity',
    hover_data=['Product Name'],
    title='Sales vs Profit (bubble size = Quantity)'
)
st.plotly_chart(fig7, use_container_width=True)
