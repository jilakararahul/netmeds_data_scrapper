import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV data
df = pd.read_csv("medicines_data2.csv")

# Basic Info
print("Basic Dataset Info:")
print(df.info())
print("\nFirst 5 Rows:")
print(df.head())

# Convert prices to numeric
df['final_price'] = df['final_price'].str.replace('₹', '').str.replace(',', '').astype(float)
df['mrp'] = df['mrp'].str.replace('₹', '').str.replace(',', '').astype(float)

# Calculate discount % (if missing or inconsistent)
df['calculated_discount'] = round(100 * (df['mrp'] - df['final_price']) / df['mrp'], 2)

# Clean rating
def clean_rating(r):
    try:
        return float(r)
    except:
        return None

df['rating'] = df['rating'].apply(clean_rating)

# Split categories
df['category_list'] = df['categories'].str.split(',')

# --- Analysis ---

# 1. Price Analysis
print("\nAverage Prices:")
print(df[['final_price', 'mrp']].mean())

# 2. Discount Summary
print("\nDiscount Stats:")
print(df['calculated_discount'].describe())

# 3. Rating Overview
print("\nRating Stats:")
print(df['rating'].describe())

# 4. Top Manufacturers
print("\nTop Manufacturers:")
print(df['manufacturer'].value_counts())

# --- Visuals ---

sns.set(style="whitegrid")

# Discount distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['calculated_discount'], bins=10, kde=True)
plt.title("Discount Distribution")
plt.xlabel("Discount (%)")
plt.ylabel("Product Count")
plt.tight_layout()
plt.savefig("discount_distribution.png")

# Ratings distribution
plt.figure(figsize=(6, 4))
sns.countplot(x='rating', data=df)
plt.title("Ratings Distribution")
plt.tight_layout()
plt.savefig("ratings_distribution.png")

# Price vs. Discount scatter
plt.figure(figsize=(8, 5))
sns.scatterplot(x='final_price', y='calculated_discount', hue='manufacturer', data=df)
plt.title("Final Price vs Discount %")
plt.tight_layout()
plt.savefig("price_vs_discount.png")

print("\nAnalysis complete. Charts saved as PNG files.")
