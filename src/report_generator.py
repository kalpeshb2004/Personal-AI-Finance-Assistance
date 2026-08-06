import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from src.categorizer import get_matched_keyword


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


# Kuch specific keywords ko ek common label ke niche group karna hai (jaise sab hotels)
GROUP_LABELS = {
    "oyo": "Hotel Booking",
    "taj hotels": "Hotel Booking",
    "marriott": "Hotel Booking",
    "hilton": "Hotel Booking",
    "airbnb": "Hotel Booking",
    "treebo": "Hotel Booking",
    "fabhotels": "Hotel Booking",
    "agoda": "Hotel Booking",
    "booking.com": "Hotel Booking",
    "trivago": "Hotel Booking",
    "hotel": "Hotel Booking",
    "resort": "Hotel Booking",
}


def group_keyword(keyword):
    return GROUP_LABELS.get(keyword, keyword)


def generate_pdf_report(df, account_details, output_path="reports/finance_report.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # ---------- Title ----------
    story.append(Paragraph("Personal Finance Report", styles["Title"]))
    story.append(Spacer(1, 12))
    
    # ---------- Account Details Section ----------
    story.append(Paragraph("Account Details", styles["Heading2"]))
    
    account_info = [
        ["Name", account_details.get("Name", "N/A")],
        ["Account No", account_details.get("AccountNo", "N/A")],
        ["Bank Name", account_details.get("BankName", "N/A")],
        ["Branch", account_details.get("Branch", "N/A")],
        ["IFSC", account_details.get("IFSC", "N/A")],
        ["Address", account_details.get("Address", "N/A")],
    ]
    
    account_table = Table(account_info, colWidths=[120, 350])
    account_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(account_table)
    story.append(Spacer(1, 20))
    
    # ---------- Spending Summary Section ----------
    story.append(Paragraph("Spending Summary", styles["Heading2"]))
    
    spend_df = df[df["Withdrawal"] > 0]
    total_spend = spend_df["Withdrawal"].sum()
    
    # Statement ka date range nikalo — kitne mahine ka data hai
    start_date = df["Date"].min()
    end_date = df["Date"].max()
    
    # Mahine count karo (partial month bhi 1 count hoga)
    months_covered = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
    
    date_range_str = f"{start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}"
    
    summary_info = [
        ["Total Spending", f"Rs. {total_spend:,.2f}"],
        ["Total Transactions", str(len(df))],
        ["Date Range", date_range_str],
        ["Months Covered", f"{months_covered} month(s)"],
    ]
    summary_table = Table(summary_info, colWidths=[150, 200])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # ---------- Category Breakdown Table ----------
    story.append(Paragraph("Category-wise Spending", styles["Heading2"]))
    
    non_transfer_df = spend_df[spend_df["Category"] != "Person Transfer"]
    category_totals = non_transfer_df.groupby("Category")["Withdrawal"].sum().sort_values(ascending=False)
    
    cat_data = [["Category", "Amount"]]
    
    transfer_df = df[df["Category"] == "Person Transfer"]
    total_sent = transfer_df["Withdrawal"].sum()
    total_received = transfer_df["Deposit"].sum()
    
    if total_sent > 0 or total_received > 0:
        cat_data.append(["Person Transfer (Sent)", f"Rs. {total_sent:,.2f}"])
        cat_data.append(["Person Transfer (Received)", f"Rs. {total_received:,.2f}"])
    
    for cat, amt in category_totals.items():
        cat_data.append([cat, f"Rs. {amt:,.2f}"])
    
    cat_table = Table(cat_data, colWidths=[200, 150])
    cat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 20))

    # ---------- Category-wise App/Merchant Breakdown (sabhi categories ke liye) ----------
    skip_categories = ["Person Transfer", "Uncategorized"]
    
    all_categories = spend_df["Category"].unique()
    
    for category in sorted(all_categories):
        if category in skip_categories:
            continue
        
        cat_spend_df = spend_df[spend_df["Category"] == category].copy()
        
        if cat_spend_df.empty:
            continue
        
        cat_spend_df["App"] = cat_spend_df["CleanMerchant"].apply(get_matched_keyword)
        cat_spend_df["App"] = cat_spend_df["App"].apply(group_keyword)   # <- hotel jaisi grouping yahi apply hoti hai
        
        app_totals = cat_spend_df.groupby("App")["Withdrawal"].sum().sort_values(ascending=False)
        
        story.append(Paragraph(f"{category} - Breakdown", styles["Heading3"]))
        
        app_data = [["Merchant/App", "Amount"]] + [[app.title(), f"Rs. {amt:,.2f}"] for app, amt in app_totals.items()]
        
        app_table = Table(app_data, colWidths=[200, 150])
        app_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#70AD47")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(app_table)
        story.append(Spacer(1, 14))
    
    # ---------- Charts ----------
    story.append(Paragraph("Spending Charts", styles["Heading2"]))
    try:
        story.append(Image("reports/category_pie.png", width=4*inch, height=3*inch))
        story.append(Spacer(1, 12))
        story.append(Image("reports/category_bar.png", width=5*inch, height=3.5*inch))
    except Exception:
        story.append(Paragraph("(Charts not available)", styles["Normal"]))
    
    story.append(Spacer(1, 20))
    
    
    doc.build(story)
    print(f"PDF report saved to {output_path}")