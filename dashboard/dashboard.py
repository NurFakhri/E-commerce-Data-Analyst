import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul Dashboard
st.title("E-Commerce Dashboard")
st.subheader("Data Overview and Analysis")

# Membaca dataset dengan st.cache_data
@st.cache_data
def load_data():
    return pd.read_csv("maindata.csv")

data = load_data()

# Filter berdasarkan country (dropdown)
country_filter = st.sidebar.selectbox(
    "Select Country", 
    options=["All Country"] + list(data["customer_state"].unique()),  # Menambahkan "All Country"
    index=0 
)

# Memfilter data berdasarkan input pengguna
if country_filter == "All Country":
    data_filtered = data  # Tidak ada filter negara, gunakan semua data
else:
    data_filtered = data[data["customer_state"] == country_filter]  # Filter berdasarkan negara

# --- CARD: Total Sales ---
total_sales = data_filtered["price"].sum()
col1, col2 = st.columns([1, 2])

with col1:
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")

# --- PIE CHART: Percentage of Delivered Orders ---
order_status_counts = data_filtered["order_status"].value_counts()
delivered_count = order_status_counts.get("delivered", 0)
total_orders = order_status_counts.sum()

if total_orders > 0:
    delivered_percentage = (delivered_count / total_orders) * 100
else:
    delivered_percentage = 0

fig_pie, ax_pie = plt.subplots()
ax_pie.pie(
    [delivered_percentage, 100 - delivered_percentage],
    labels=["Delivered", "Others"],
    autopct='%1.1f%%',
    startangle=90,
    colors=["green", "gray"]
)
ax_pie.set_title("Percentage of Delivered Orders")
st.pyplot(fig_pie)

# --- TOP 10 Product Categories by Sales ---
category_sales = data_filtered.groupby("product_category_name")["price"].sum().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(10, 5))
category_sales.plot(kind="bar", color="skyblue", ax=ax1)
ax1.set_title("Top 10 Product Categories by Sales")
ax1.set_ylabel("Total Sales")
ax1.set_xlabel("Product Category")
plt.xticks(rotation=45)
st.pyplot(fig1)

# --- TOP 10 HIGH REVIEW PRODUCTS ---
high_reviews = data_filtered[data_filtered["review_score"] >= 4]
high_review_products = high_reviews.groupby("product_category_name")["review_score"].count().sort_values(ascending=False).head(10)

fig_high, ax_high = plt.subplots(figsize=(10, 5))
high_review_products.plot(kind="bar", color="green", ax=ax_high)
ax_high.set_title("Top 10 High Review Products")
ax_high.set_ylabel("Review Count")
ax_high.set_xlabel("Product Category")
plt.xticks(rotation=45)
st.pyplot(fig_high)

# --- TOP 10 LOW REVIEW PRODUCTS ---
low_reviews = data_filtered[data_filtered["review_score"] <= 2]
low_review_products = low_reviews.groupby("product_category_name")["review_score"].count().sort_values(ascending=False).head(10)

fig_low, ax_low = plt.subplots(figsize=(10, 5))
low_review_products.plot(kind="bar", color="red", ax=ax_low)
ax_low.set_title("Top 10 Low Review Products")
ax_low.set_ylabel("Review Count")
ax_low.set_xlabel("Product Category")
plt.xticks(rotation=45)
st.pyplot(fig_low)

# --- TOTAL SALES BY COUNTRY ---
total_sales_by_country = data.groupby("customer_state")["price"].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(10, 5))
total_sales_by_country.plot(kind="bar", color="orange", ax=ax2)
ax2.set_title("Total Sales by Country")
ax2.set_ylabel("Total Sales")
ax2.set_xlabel("Country")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Menampilkan data tabel
st.write("Preview Data", data_filtered.head())
