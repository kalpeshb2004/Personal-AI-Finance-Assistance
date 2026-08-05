import pdfplumber
import pandas as pd

def extract_transactions_from_pdf(pdf_path):
    all_rows = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    all_rows.append(row)
    
    # Sirf valid transaction rows rakho
    # Condition: pehla column '#' ka number ho (1,2,3...) — header/junk mein ye nahi hota
    transactions = []
    for row in all_rows:
        if row[0] and row[0].strip().isdigit():
            transactions.append(row)
    
    # DataFrame banao
    columns = ["SNo", "Date", "Description", "RefNo", "Withdrawal", "Deposit", "Balance"]
    df = pd.DataFrame(transactions, columns=columns)
    
    # Multi-line description ko single line karo
    df["Description"] = df["Description"].str.replace("\n", " ")
    
    return df

if __name__ == "__main__":
    df = extract_transactions_from_pdf("data/AccountStatement_01-Aug-2026_03-Aug-2026.pdf")
    print(df)
    df.to_csv("data/cleaned_statement.csv", index=False)
    print("\nSaved to data/cleaned_statement.csv")
    