# Excel Report Generator
# Ek Excel file, 3 sheets ke saath — Transactions (poora raw data), Summary (category-wise total), Stats (overall spending/income/savings).

import pandas as pd

def generate_excel_report(df, output_path="reports/finance_report.xlsx"):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        
        # Sheet 1: Raw transactions
        df.to_excel(writer, sheet_name="Transactions", index=False)
        
        # Sheet 2: Category-wise summary
        spend_df = df[df["Withdrawal"] > 0]
        summary = spend_df.groupby("Category")["Withdrawal"].sum().sort_values(ascending=False)
        summary = summary.reset_index()
        summary.columns = ["Category", "Total Spent"]
        summary.to_excel(writer, sheet_name="Summary", index=False)
        
        # Sheet 3: Overall stats
        total_spend = spend_df["Withdrawal"].sum()
        total_income = df["Deposit"].sum()
        stats = pd.DataFrame({
            "Metric": ["Total Spending", "Total Income", "Net Savings", "Total Transactions"],
            "Value": [total_spend, total_income, total_income - total_spend, len(df)]
        })
        stats.to_excel(writer, sheet_name="Stats", index=False)
    
    print(f"Excel report saved to {output_path}")