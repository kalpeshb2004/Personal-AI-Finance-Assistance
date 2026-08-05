import matplotlib.pyplot as plt

# Spending Visualization
def plot_category_pie(df, save_path="reports/category_pie.png"):
    # Sirf spending (Withdrawal) wale rows lo, deposits nahi
    spend_df = df[df["Withdrawal"] > 0]
    
    category_totals = spend_df.groupby("Category")["Withdrawal"].sum()
    
    plt.figure(figsize=(8, 6))
    plt.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
    plt.title("Spending by Category")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Pie chart saved to {save_path}")

def plot_category_bar(df, save_path="reports/category_bar.png"):
    spend_df = df[df["Withdrawal"] > 0]
    category_totals = spend_df.groupby("Category")["Withdrawal"].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    category_totals.plot(kind="bar", color="skyblue")
    plt.title("Total Spending by Category")
    plt.ylabel("Amount (₹)")
    plt.xlabel("Category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Bar chart saved to {save_path}")