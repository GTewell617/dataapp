import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, October 6th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('ME')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

# **1** Category dropdown
categories = sorted(df["Category"].unique())
selected_category = st.selectbox("Select a Category", categories)

# Keeping rows that match the selected category
category_df = df[df["Category"] == selected_category]

# **2** Multiselect for Sub_Category within the selected Category
sub_categories = sorted(category_df["Sub_Category"].unique())
selected_subs = st.multiselect("Select Sub-Categories", sub_categories)

# Keep rows only where Sub Category is selected
sub_df = category_df[category_df["Sub_Category"].isin(selected_subs)]

# **3** Line chart of monthly sales for the selected Sub-Categories
if selected_subs:
    sales_by_month_sub = (
        sub_df.groupby([pd.Grouper(freq="ME"), "Sub_Category"])["Sales"]
        .sum()
        .unstack()
        .fillna(0)
    )
    st.line_chart(sales_by_month_sub)
        # **4** Adding three metrics for the selected Sub-Categories
    total_sales = sub_df["Sales"].sum()
    total_profit = sub_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100
        # **5** Overall profit margin across all products
    overall_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    margin_delta = profit_margin - overall_margin
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin", f"{profit_margin:.2f}%", delta=f"{margin_delta:.2f}%")
else:
    st.info("Select at least one Sub-Category to see the chart.")
