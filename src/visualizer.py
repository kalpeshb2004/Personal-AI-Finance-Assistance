import matplotlib.pyplot as plt

# Spending Visualization
def plot_category_pie(df, save_path="reports/category_pie.png"):
    # Sirf real spending categories lo — Person Transfer exclude karo (wo transfer hai, spending nahi)
    spend_df = df[(df["Withdrawal"] > 0) & (df["Category"] != "Person Transfer")]
    
    category_totals = spend_df.groupby("Category")["Withdrawal"].sum().sort_values(ascending=False)
    
    if category_totals.empty:
        print("No spending data to plot (excluding Person Transfer)")
        return
    
    plt.figure(figsize=(9, 7))
    
    colors_list = plt.cm.tab20.colors
    
    wedges, texts, autotexts = plt.pie(
        category_totals,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors_list,
        pctdistance=0.8,
    )
    
    # Labels ko pie ke bahar legend mein daalo (overlap avoid karne ke liye)
    plt.legend(
        wedges,
        category_totals.index,
        title="Category",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=9,
    )
    
    plt.title("Spending by Category (excluding Person Transfer)")
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"Pie chart saved to {save_path}")


def plot_category_bar(df, save_path="reports/category_bar.png"):
    # Bar chart bhi Person Transfer exclude karke banate hain, consistency ke liye
    spend_df = df[(df["Withdrawal"] > 0) & (df["Category"] != "Person Transfer")]
    category_totals = spend_df.groupby("Category")["Withdrawal"].sum().sort_values(ascending=False)
    
    if category_totals.empty:
        print("No spending data to plot (excluding Person Transfer)")
        return
    
    plt.figure(figsize=(10, 6))
    category_totals.plot(kind="bar", color="skyblue")
    plt.title("Total Spending by Category (excluding Person Transfer)")
    plt.ylabel("Amount (Rs.)")
    plt.xlabel("Category")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Bar chart saved to {save_path}")