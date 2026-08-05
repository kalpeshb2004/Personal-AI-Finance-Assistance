import pandas as pd
import re
from src.pdf_parser import extract_transactions_from_pdf  # PDF wala function import karo

def clean_amount_column(df, column_name):
    df[column_name] = df[column_name].astype(str).str.replace(",", "", regex=False).str.strip()
    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    df[column_name] = df[column_name].fillna(0)
    return df

def clean_merchant_name(description):
    text = description.lower()
    text = re.sub(r'upi[/\-]', '', text)
    text = re.sub(r'\b\d{6,}\b', '', text)
    text = re.sub(r'[/\-]', ' ', text)
    text = re.sub(r'\b(payment from|payment for|pay via|na)\b', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_and_clean(file_path):
    # File type check karo — PDF hai ya CSV
    if file_path.lower().endswith(".pdf"):
        df = extract_transactions_from_pdf(file_path)
    else:
        df = pd.read_csv(file_path)
    
    df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")
    
    df = clean_amount_column(df, "Withdrawal")
    df = clean_amount_column(df, "Deposit")
    df = clean_amount_column(df, "Balance")
    
    df["CleanMerchant"] = df["Description"].apply(clean_merchant_name)
    
    print(df[["Description", "CleanMerchant"]])
    
    return df

if __name__ == "__main__":
    df = load_and_clean("data/AccountStatement_01-Aug-2026_03-Aug-2026.pdf")