# Simple flow: Raw CSV → Date fix → Amount fix → Merchant name clean → Final ready DataFrame.

import pandas as pd
import re

# Ek numeric column (Withdrawal/Deposit/Balance) ko clean float mein convert karta hai.
def clean_amount_column(df, column_name):
    df[column_name] = df[column_name].astype(str).str.replace(",", "", regex=False).str.strip() # (, . " ") ye hatana iska kam
    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    df[column_name] = df[column_name].fillna(0)
    return df

# Raw transaction description se merchant ka clean naam nikalta hai (regex se noise hatake).
def clean_merchant_name(description):
    text = description.lower()
    text = re.sub(r'upi[/\-]', '', text)
    text = re.sub(r'\b\d{6,}\b', '', text)
    text = re.sub(r'[/\-]', ' ', text)
    text = re.sub(r'\b(payment from|payment for|pay via|na)\b', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Master function — poora pipeline chalata hai, upar ke dono functions ko call karke final clean DataFrame banata hai.
def load_and_clean(file_path):
    df = pd.read_csv(file_path)
    
    df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")
    
    df = clean_amount_column(df, "Withdrawal")
    df = clean_amount_column(df, "Deposit")
    df = clean_amount_column(df, "Balance")
    
    df["CleanMerchant"] = df["Description"].apply(clean_merchant_name)
    
    print(df[["Description", "CleanMerchant"]])
    
    return df

if __name__ == "__main__":
    df = load_and_clean("data/cleaned_statement.csv")


