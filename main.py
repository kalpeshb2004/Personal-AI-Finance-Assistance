from src.data_loader import load_and_clean
from src.categorizer import categorize_dataframe
import pandas as pd


pd.set_option('display.colheader_justify', 'left')

df = load_and_clean("data/cleaned_statement.csv")
df = categorize_dataframe(df)

print(df[["CleanMerchant", "Category"]])
print(df.to_markdown(index=False))