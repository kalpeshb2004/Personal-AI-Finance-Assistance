from src.data_loader import load_and_clean       # CSV load + cleaning wala function
from src.categorizer import categorize_dataframe  # Rule+fuzzy+pattern categorization wala function
import pandas as pd
from src.visualizer import plot_category_pie, plot_category_bar  # Chart banane wale functions

pd.set_option('display.colheader_justify', 'left')  # Sirf terminal print ke header ko left-align karega (cosmetic)

df = load_and_clean("data/cleaned_statement.csv")   # Raw CSV -> clean DataFrame (Date, Amount, Merchant sab fix)
df = categorize_dataframe(df)                        # Har transaction ko category assign karo (Category + MatchType column add hoga)

print(df[["CleanMerchant", "Category"]])              # Sirf 2 columns dikhao quick check ke liye
print(df.to_markdown(index=False))                    # Poora DataFrame table format mein terminal pe dikhao (index number chhupa ke)

plot_category_pie(df)   # Category-wise spending ka pie chart banao, reports/ folder mein PNG save hogi
plot_category_bar(df)   # Category-wise spending ka bar chart banao, reports/ folder mein PNG save hogi

