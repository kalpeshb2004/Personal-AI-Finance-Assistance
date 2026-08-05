from src.categories import MERCHANT_RULES

def categorize_by_keyword(clean_merchant_text):
    for keyword, category in MERCHANT_RULES.items():
        if keyword in clean_merchant_text:
            return category
    return "Uncategorized"

def categorize_dataframe(df):
    df["Category"] = df["CleanMerchant"].apply(categorize_by_keyword)
    return df