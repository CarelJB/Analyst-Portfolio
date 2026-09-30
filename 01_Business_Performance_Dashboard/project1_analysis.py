import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Base paths
project_folder = Path(r"C:\Users\jacob\projects\Analyst-Portfolio\01_Business_Performance_Dashboard")
file_path = project_folder / "data_clean" / "clean_business_data.xlsx"
images_folder = project_folder / "images"

# Read clean data
df = pd.read_excel(file_path, sheet_name="Clean_Data")

# Basic cleanup
df["Date"] = pd.to_datetime(df["Date"])

# KPI calculations
total_revenue = df["Revenue"].sum()
total_gross_profit = df["Gross_Profit"].sum()
gross_margin_pct = total_gross_profit / total_revenue
avg_revenue_per_transaction = df["Revenue"].mean()
num_customers = df["Customer"].nunique()

print("=== KPI SUMMARY ===")
print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Gross Profit: {total_gross_profit:,.2f}")
print(f"Gross Margin %: {gross_margin_pct:.2%}")
print(f"Number of Customers: {num_customers}")
print(f"Avg Revenue / Transaction: {avg_revenue_per_transaction:,.2f}")

# Monthly summary
df["Month"] = df["Date"].dt.to_period("M").astype(str)
monthly_summary = (
    df.groupby("Month")[["Revenue", "Gross_Profit"]]
    .sum()
    .reset_index()
)

print("\n=== MONTHLY SUMMARY ===")
print(monthly_summary)

# Revenue by category
category_summary = (
    df.groupby("Category")[["Revenue", "Gross_Profit"]]
    .sum()
    .sort_values("Revenue", ascending=False)
    .reset_index()
)

print("\n=== CATEGORY SUMMARY ===")
print(category_summary)

# Top customers by revenue
top_customers = (
    df.groupby("Customer")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

print("\n=== TOP 10 CUSTOMERS BY REVENUE ===")
print(top_customers)

# Create Monthly Revenue chart
plt.figure(figsize=(10, 5))
plt.plot(monthly_summary["Month"], monthly_summary["Revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
output_chart = images_folder / "monthly_revenue_trend_python.png"
plt.savefig(output_chart, dpi=150)
plt.close()

print(f"\nChart saved successfully: {output_chart}")