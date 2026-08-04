import pandas as pd

def load_statement(file_path):
    df = pd.read_csv(file_path)
    
    print("Columns found:", df.columns.tolist())
    print("\nShape:", df.shape)
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values:")
    print(df.isnull().sum())
    
    return df

if __name__ == "__main__":
    df = load_statement("data/sample_statement.csv")