# Person Transfer Category
import re
from src.categories import MERCHANT_RULES

def categorize_by_keyword(clean_merchant_text):
    for keyword, category in MERCHANT_RULES.items():
        if keyword in clean_merchant_text:
            return category
    return None  # ab None return karo, "Uncategorized" nahi

def is_person_transfer(description):
    # Pattern: "Payment from"/"Payment for" ke saath, aur koi known merchant keyword nahi
    text = description.lower()
    if "payment from" in text or "payment for" in text:
        return True
    return False

def categorize_row(row):
    category = categorize_by_keyword(row["CleanMerchant"])
    if category:
        return category
    if is_person_transfer(row["Description"]):
        return "Person Transfer"
    return "Uncategorized"

def categorize_dataframe(df):
    df["Category"] = df.apply(categorize_row, axis=1)
    return df