import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.title("📊 Sales Analytics Dashboard")

# LOAD DATA
df = pd.read_csv("sales.csv")

# Keep original data safe
df["Category"] = df["Category"].astype(str)
category_map = {

    # Electronics
    "4K Monitor":"Electronics",
    "Action Camera":"Electronics",
    "Bluetooth Speaker":"Electronics",
    "Car Charger":"Electronics",
    "Drone Mini":"Electronics",
    "External HDD 2TB":"Electronics",
    "Gaming Mouse":"Electronics",
    "Graphic Tablet":"Electronics",
    "HDMI Cable 2m":"Electronics",
    "Laptop Sleeve":"Electronics",
    "Mechanical Keyboard":"Electronics",
    "Memory Card 128GB":"Electronics",
    "Microphone":"Electronics",
    "Noise Cancelling Headphones":"Electronics",
    "Phone Tripod":"Electronics",
    "Portable SSD 1TB":"Electronics",
    "Power Bank 20000mAh":"Electronics",
    "Projector Mini":"Electronics",
    "Router":"Electronics",
    "Smart Light Bulb":"Electronics",
    "Smartphone Case":"Electronics",
    "Smartwatch":"Electronics",
    "USB-C Charger":"Electronics",
    "Webcam Full HD":"Electronics",
    "Wireless Charger":"Electronics",
    "Wireless Earbuds":"Electronics",

    # Books
    "Children's Book":"Books",
    "Novel Bestseller":"Books",

    # Clothing
    "Dress Shirt":"Clothing",
    "Jeans":"Clothing",
    "Running Shoes":"Clothing",
    "Sunglasses":"Clothing",
    "T-Shirt":"Clothing",
    "Winter Jacket":"Clothing",

    # Home & Kitchen
    "Air Fryer":"Home & Kitchen",
    "Cookware Set":"Home & Kitchen",
    "Desk Organizer":"Home & Kitchen",
    "Desk Plant":"Home & Kitchen",
    "Electric Kettle":"Home & Kitchen",
    "Instant Pot":"Home & Kitchen",
    "LED Desk Lamp":"Home & Kitchen",
    "Office Chair":"Home & Kitchen",
    "Vacuum Cleaner":"Home & Kitchen",

    # Sports & Outdoors
    "Backpack":"Sports & Outdoors",
    "Fitness Band":"Sports & Outdoors",
    "Water Bottle":"Sports & Outdoors",
    "Yoga Mat":"Sports & Outdoors",

    # Toys & Games
    "Board Game":"Toys & Games",
    "Kids Toy Car":"Toys & Games",
    "Puzzle 1000pc":"Toys & Games"
}

df["Category"] = df["ProductName"].map(category_map).fillna(df["Category"])


# CLEAN DATA
df["EstimateProfit"] = df["TotalAmount"] - df["Tax"] - df["ShippingCost"] - df["Discount"]

df["OrderDate"] = pd.to_datetime(df["OrderDate"])

df["Month"] = df["OrderDate"].dt.month_name()

# =========================
# FIX 1: MONTH ORDER (IMPORTANT)
# =========================
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

# =========================
# FILTER (KEEP ALL CITIES OPTION)
# =========================
# PAGE SETUP
st.sidebar.title("⚙️ Analytics Controls")

# City
with st.sidebar.expander("🏙️ City", expanded=False):

    city = st.selectbox(
        "Choose a City",
        ["All"] + list(df["City"].unique())
    )

if city != "All":
    df = df[df["City"] == city]


# Category
with st.sidebar.expander("📦 Category", expanded=False):

    category = st.selectbox(
        "Choose Category",
        ["All"] + list(df["Category"].unique())
    )

if category != "All":
   df = df[df["Category"] == category]
# st.subheader("Debug Check")
# st.write(df[["ProductName", "Category"]].drop_duplicates())


# Date
with st.sidebar.expander("📅 Date", expanded=False):

 start_date = st.date_input(
    "Start Date",
    value=df["OrderDate"].min(),
    min_value=df["OrderDate"].min(),
    max_value=df["OrderDate"].max()
) 

 end_date = st.date_input(
    "End Date",
    value=df["OrderDate"].max(),
    min_value=df["OrderDate"].min(),
    max_value=df["OrderDate"].max()
)

df = df[
    (df["OrderDate"] >= pd.to_datetime(start_date)) &
    (df["OrderDate"] <= pd.to_datetime(end_date))
]
# check dataset date
# st.write("First Date :", df["OrderDate"].min())
# st.write("Last Date :", df["OrderDate"].max())

# =========================
# KPI
# =========================
st.subheader("📌 Key Metrics")
# =========================
# KPI
# =========================

city_sales = df.groupby("City")["TotalAmount"].sum()

top_city = city_sales.idxmax()
top_city_sales = city_sales.max()

city_profit = df.groupby("City")["EstimateProfit"].sum()

top_profit_city = city_profit.idxmax()
top_profit = city_profit.max()

least_product = df.groupby("ProductName")["TotalAmount"].sum().idxmin()

best_month = df.groupby("Month")["TotalAmount"].sum().idxmax()


col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Sales",
    f"{df['TotalAmount'].sum():,.0f}"
)

col2.metric(
    "Top Sales City",
    top_city
)

col3.metric(
    "Sales Amount",
    f"{top_city_sales:,.0f}"
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "Highest Profit City",
    top_profit_city
)

col5.metric(
    "Profit Amount",
    f"{top_profit:,.0f}"
)

col6.metric(
    "Least Sold Product",
    least_product
)

st.metric(
    "Best Sales Month",
    best_month
)
# =========================
# BAR CHART (CITY - FIXED)
# =========================
st.subheader("🏙️ City Sales")

city_sales = df.groupby("City")["TotalAmount"].sum().reset_index()

fig1 = px.bar(
    city_sales,
    x="City",
    y="TotalAmount",
    color="City",
    title="City Wise Sales"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# MONTHLY SALES (FIXED ORDER)
# =========================
st.subheader("📈 Monthly Sales")

month_sales = df.groupby("Month")["TotalAmount"].sum().reset_index()

fig2 = px.line(
    month_sales,
    x="Month",
    y="TotalAmount",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# PIE CHART (ADDED BACK)
# =========================
st.subheader("🥧 Top 5 Cities")

top5 = city_sales.sort_values("TotalAmount", ascending=False).head(5)

fig3 = px.pie(
    top5,
    names="City",
    values="TotalAmount",
    title="Top 5 City Contribution" 
)

st.plotly_chart(fig3, use_container_width=True) 
st.caption("Created by Navin Sakthi Vel | Streamlit + Plotly")