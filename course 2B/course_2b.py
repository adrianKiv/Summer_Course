# -*- coding: utf-8 -*-
"""Course 2B.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ihZrpvlJhfvEAM9mXhTKMLDeHlhk7hyP

**Group 21 Course 2B Assigment**

*   Muhammad Fikri Kafilli
*   Adrian Mulianto
*   Ndidiamaka okpala
*   Hamid Khan
*   Della Putri Wahyuni
*   Mochamad Rizky Farhan Auliya

Exploring the data Sales involves a step-by-step process:

1. Check and prepare data to clean and handling missing values and ensuring consistency.
2. Summaries the data with statistical analysis: Use descriptive statistics with aggregation function (i.e sum, count, average, min, max) for searching meaningful information such as: top product sales, total amount, average amount, etc
3. Use Statistical methods to identify significant correlation/comparative/distribution/trending between variables from the data
4. Visualize the data with charts and graphs to see patterns and relationships (min.3 graph)
5. Use related python library to handle all of tasks
6. Upload your source code with python extension file such as .py or .ipynb and file .rawgraphs (if you visualized the data using rawgraphs)
7. Tomorrow some of you will present the result of your assignment

# First Steps (importing all requirement)

Import all library you need
"""

import pandas as pd #
import numpy as np #
import matplotlib.pyplot as plt #
import seaborn as sns #

"""Import dataset
This code run with google colab so using this path as default. Change if needed
"""

dataset_path = "/content/orderdataset.csv"
order_test_df = pd.read_csv(dataset_path)

"""test. If path working you can see the table"""

order_test_df.head()

"""as we can see here data is not normal format for csv (because is not separated by comma but with semicolon so we need to change that). We have 2 option (as far as we know)

1.   Just use sep=";" argument on pd.read_csv() so pandas will read semicolon just like read using comma (what we doing here is this) or,
2.   Convert first using to_csv() and just use new csv with comma as separator for code.


"""

order_df = pd.read_csv(dataset_path, sep=";")

order_df.head()

"""As now we can see here, we can read the table like normal table. Now we move to next step

# Data Cleaning

## Check data for cleaning
"""

# check how much data in here
order_df.info()

"""As we can see here we have missing data. On product_weight_gram is just 49980 so missing like 19 data. Now we check for data duplication, we can clean that later."""

print("Sum duplicate data : ", order_df.duplicated().sum())

"""We don't have any data is duplicated. So next is checking anomaly on data (like wierd input)"""

order_df.describe()

"""Nothing wierd in here

## Cleaning data missing

Because we have 19 data missing we can check now what missing
"""

order_df[order_df.product_weight_gram.isna()]

"""We have some option to clean it

1.   We can just drop all NaN data and do all that without NaN data
2.   We can use some smart guess (using value we have) for filling NaN data we have.

### Trying smart guess

We can try using some smart guess. We have product_id in here. If product_id who have NaN value is same as product_id with value on product_weight_gram we can just cross reference and fill NaN value. We need to check first if we have another duplicate product_id
"""

product_ids_with_nan = order_df[order_df.product_weight_gram.isna()]['product_id'].unique()
print(product_ids_with_nan)

order_df[order_df['product_id'] == '09ff539a621711667c43eba6a3bd8466']

order_df[order_df['product_id'] == '5eb564652db742ff8f28759cd8d2652a']

"""as we can check we have 2 product_id who have NaN value and that 2 product_id is unique only for NaN value so we can just simply drop NaN value because we cannot check what item in there

### Just drop the table
"""

order_df.dropna(subset=['product_weight_gram'], inplace=True)

"""Check data if still have data missing"""

order_df.isna().sum()

"""We don't have any data missing anymore

# Explanitory Data Analysis (EDA)
"""

order_df.describe(include="all")

"""Check for how much sales base on category"""

order_df.groupby(by="product_category_name").agg({
  "order_id": "nunique",
  "quantity" : "sum",
  "price": "sum"
})

"""As we can see automotive category bringing the most revenue with 16.487.385.000 but for most item sold by quantity or order we have toys category at 7703 item sold and 6204 item order.

Checking how much is freight value based on product category
"""

order_df.groupby(by="product_category_name").agg({
  "order_id": "nunique",
  "freight_value" : ["sum", "mean"],
  "price": "sum"
})

order_df.groupby(by="payment_type").agg({
  "order_id": "nunique",
  "freight_value" : ["sum", "mean"],
  "price": "sum"
})

order_df.groupby(by="product_category_name").agg({
  "order_id": "nunique",
  "price": ["min", "max", "mean", "std"]
})

# Analisis Deskriptif
min_value = order_df['quantity'].min()
max_value = order_df['quantity'].max()
range_value = max_value - min_value
mean_value = order_df['quantity'].mean()
median_value = order_df['quantity'].median()
variance_value = order_df['quantity'].var()
std_dev_value = order_df['quantity'].std()

print(f"The minimum quantity is {min_value}")
print(f"The maximum quantity is {max_value}")
print(f"The range of quantity is {range_value}")
print(f"The mean quantity is {mean_value:.2f}")
print(f"The median quantity is {median_value}")
print(f"The variance of quantity is {variance_value:.2f}")
print(f"The standard deviation of quantity is {std_dev_value:.2f}")

order_df.info()

# Selecting numerical columns for correlation analysis
numerical_cols = ['quantity', 'price', 'freight_value', 'product_weight_gram']

# Calculate correlation matrix
correlation_matrix = order_df[numerical_cols].corr()

# Plot heatmap of correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('Correlation Matrix of Numerical Variables')
plt.show()

# Group data based on product_category_name and sum the total quantity.
category_sales = order_df.groupby('product_category_name')['quantity'].sum().reset_index()

# Setting up data for pie charts
labels = category_sales['product_category_name']
sizes = category_sales['quantity']

# Creating pie chart
plt.figure(figsize=(10, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Proportion of Quantity Sold by Product Category')
plt.axis('equal')  # Making sure the pie chart circle is circular
plt.show()

# DISPLAYS THE NUMBER OF ITEMS SOLD BY DATE

# Convert the purchase_date column to datetime type
order_df['purchase_date'] = pd.to_datetime(order_df['purchase_date'], dayfirst=True)

# Group data by date and sum the quantity column
daily_sales = order_df.groupby('purchase_date')['quantity'].sum().reset_index()

# Display results in table form
print(daily_sales)

# Display results in graph form
plt.figure(figsize=(14, 7))
plt.plot(daily_sales['purchase_date'], daily_sales['quantity'], marker='o')
plt.title('Daily Quantity Sold')
plt.xlabel('Purchase Date')
plt.ylabel('Quantity Sold')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# merge data by month and display the total price (price * quantity) using a bar plot every month

# Convert the purchase_date column to datetime type
order_df['purchase_date'] = pd.to_datetime(order_df['purchase_date'], dayfirst=True)

# Extract the year and month from the purchase_date field
order_df['year_month'] = order_df['purchase_date'].dt.to_period('M')

# Create a new column containing the total price (price * quantity)
order_df['total_price'] = order_df['price'] * order_df['quantity']

# Group the data by year and month, then add up the total prices.
monthly_sales = order_df.groupby('year_month')['total_price'].sum().reset_index()

# Display results in table form
print(monthly_sales)

# Display results in the form of a bar plot
plt.figure(figsize=(14, 7))
sns.barplot(x='year_month', y='total_price', data=monthly_sales, palette='viridis')
plt.title('Total Sales per Month')
plt.xlabel('Year-Month')
plt.ylabel('Total Sales (Price)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Convert the purchase_date column to datetime type
order_df['purchase_date'] = pd.to_datetime(order_df['purchase_date'], dayfirst=True)

# Extract the year and month from the purchase_date field
order_df['year_month'] = order_df['purchase_date'].dt.to_period('M')

# Group the data by year and month, then sum the product_weight_grams
monthly_weight = order_df.groupby('year_month')['product_weight_gram'].sum().reset_index()

# Display results in table form
print(monthly_weight)

plt.figure(figsize=(14, 7))
plt.fill_between(monthly_weight['year_month'].astype(str), monthly_weight['product_weight_gram'], color="skyblue", alpha=0.4)
plt.plot(monthly_weight['year_month'].astype(str), monthly_weight['product_weight_gram'], marker='o', color='skyblue', linewidth=2)
plt.title('Total Product Weight (gram) per Month')
plt.xlabel('Year-Month')
plt.ylabel('Total Product Weight (gram)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""# We will calculate the total revenue for each month and see the trend

## only take the data where it is not canceled or unavailable. The assumption is the product are succesfully purchased if it is not canceled or unavaliable
"""

df_approved = order_df[(order_df['order_status'] != 'canceled') & (order_df['order_status'] != 'unavailable')].copy()

df_approved['price'] = pd.to_numeric(df_approved['price'], errors='coerce')
df_approved['quantity'] = pd.to_numeric(df_approved['quantity'], errors='coerce')

df_approved['total_amount'] = df_approved['price'] * df_approved['quantity']

category_sales = df_approved.groupby('product_category_name')['quantity'].sum().reset_index()
category_sales = category_sales.rename(columns={'quantity': 'total_quantity_sold'})
most_sold_category = category_sales.sort_values(by='total_quantity_sold', ascending=False).head(8)
print("Most sold product category:\n", most_sold_category)

product_sales = df_approved.groupby('product_id')['total_amount'].sum().reset_index()
product_sales = product_sales.rename(columns={'total_amount': 'total_sales_amount'})
category_revenue = order_df.groupby('product_category_name')['total_amount'].sum().reset_index()
category_revenue = category_revenue.rename(columns={'total_amount': 'total_revenue'})
most_revenue_category = category_revenue.sort_values(by='total_revenue', ascending=False).head(8)
print("Product category with the most revenue:\n", most_revenue_category)

df_approved['purchase_date'] = pd.to_datetime(df_approved['purchase_date'], format='%d/%m/%Y')
df_approved['year'] = df_approved['purchase_date'].dt.year
df_approved['month'] = df_approved['purchase_date'].dt.month

monthly_sales = df_approved.groupby(['year', 'month'])['total_amount'].sum().reset_index()

plt.figure(figsize=(14, 8))
sns.lineplot(data=monthly_sales, x='month', y='total_amount', hue='year', marker='o')
plt.title('Monthly Sales Trend')
plt.show()