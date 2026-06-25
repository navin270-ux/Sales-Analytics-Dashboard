import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales.csv")

# print(df.head())
# print(df.info())
# print(df.isnull())
# print(df.duplicated(subset=["OrderID","OrderDate","CustomerID","CustomerName","ProductID","ProductName","Category","Brand","Quantity","UnitPrice","Discount","Tax","ShippingCost","TotalAmount","PaymentMethod","OrderStatus","City","State","Country","SellerID"]))
# print(df["TotalAmount"].sum())
# print(df.mean(numeric_only=True))
# print(df.max(numeric_only=True))
# print(df.min(numeric_only=True))

df["EstimateProfit"] = df["TotalAmount"] - df["Tax"] - df["ShippingCost"] - df["Discount"]

# print(df[["TotalAmount", "EstimateProfit"]])

city_sales=df.groupby("City")["TotalAmount"].sum()

# print(city_sales)
# print(city_sales.max())

product_sales=df.groupby("ProductName")["TotalAmount"].sum()

# print(product_sales.max())

categories=df.groupby("Category")["TotalAmount"].sum()

# print(categories.max())

city_profit=df.groupby("City")["EstimateProfit"].sum() 

# print("highest profit city")
# print(city_profit.idxmax())

# print("profit value")
# print(city_profit.max())

# print("least sell product")
# print(product_sales.idxmin())

print("========================")
print("    SALES DASHBOARD")
print("========================")

print("Total Sales :",df["TotalAmount"].sum())

print("Top Sales City :",city_sales.idxmax())
print("Sales Value :",city_sales.max())

print("Highest Profit City :",city_profit.idxmax())
print("Profit Value :",city_profit.max())

print("Least Sold Product :",product_sales.idxmin())

df["OrderDate"]=pd.to_datetime(df["OrderDate"])
df["Month"] = df["OrderDate"].dt.month_name()

month_amount = df.groupby("Month")["TotalAmount"].sum()


# print(month_amount)

order = ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]

month_amount = month_amount.reindex(order)

print("Best Sales Month :",month_amount.idxmax())
print("Monthly Sales :",month_amount.max())

print("========================")

highest_month="August"

plt.figure(figsize=(12,6))
plt.style.use("bmh")
plt.plot(month_amount.index,month_amount.values,color="darkblue",marker="o")
plt.xlabel("Month Of Sale",fontsize=12)
plt.ylabel("Total Revenue",fontsize=12)
plt.ticklabel_format(style='plain', axis='y')
plt.xticks(rotation=45)
plt.grid(alpha=0.5,color="gray")
plt.subplots_adjust(bottom=0.2,left=0.2)
plt.title("Monthly Sales Performance Dashboard",fontsize=16)

plt.scatter(
    highest_month, 
    month_amount[highest_month],
    color="green",
    s=200,
    label="Highest Sales Month"
)

plt.legend()
plt.show()

# bar chart

highest_city="Charlotte"

colors=[]

for city in city_sales.index:
    if city==highest_city:
        colors.append("green")
    else:
        colors.append("skyblue")

plt.style.use("bmh")
plt.figure(figsize=(12,6))
plt.xticks(rotation=45)
plt.subplots_adjust(bottom=0.2)

plt.bar(city_sales.index,city_sales.values,color=colors)

plt.ticklabel_format(style="plain",axis="y")
plt.xlabel("City",fontsize=12)
plt.ylabel("Total Revenue",fontsize=12)
plt.title("City-Wise Sales Analysis",fontsize=16)
plt.grid(alpha=0.5,color="gray")

plt.show()

# pie chart

top5=city_sales.sort_values(ascending=False).head(5)

highest_city="Charlotte"

a=[]

for city in top5.index:
    if city==highest_city:
        a.append("green")
    else:
        a.append("skyblue")

plt.figure(figsize=(8,8))
plt.title("City-wise Sales Distribution")

plt.pie(
    top5.values,
    labels=top5.index,
    autopct="%1.1f%%",
    colors=a,
    wedgeprops={"edgecolor":"white","linewidth":2}
)

plt.subplots_adjust(bottom=0.3)

plt.show()