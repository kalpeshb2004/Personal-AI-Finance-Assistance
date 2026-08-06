import argparse
import pandas as pd
from src.data_loader import load_and_clean
from src.categorizer import categorize_dataframe
from src.visualizer import plot_category_pie, plot_category_bar
from src.report_generator import generate_excel_report
from src.pdf_parser import extract_account_details
from src.db_operations import save_to_database
from src.report_generator import generate_excel_report, generate_pdf_report

pd.set_option('display.colheader_justify', 'left')


def run_pipeline(input_file, output_file):
    try:
        print(f"Loading file: {input_file}")
        df = load_and_clean(input_file)
    except FileNotFoundError:
        print(f"Error: File not found at {input_file}")
        return
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    
    try:
        print("Categorizing transactions...")
        df = categorize_dataframe(df)
        
        print("Generating charts...")
        plot_category_pie(df)
        plot_category_bar(df)
        
        print("Generating Excel report...")
        generate_excel_report(df, output_path=output_file)
        
        # Naya part: Agar PDF hai to account details nikalo aur DB mein save karo
        if input_file.lower().endswith(".pdf"):
            print("Extracting account details...")
            account_details = extract_account_details(input_file)
            
            print("Generating PDF report...")
            generate_pdf_report(df, account_details)
            
            print("Saving to database...")
            save_to_database(account_details, df, input_file)
        
        print("Done! Check reports/ folder.")
    except Exception as e:
        import traceback
        traceback.print_exc()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Personal Finance Bank Statement Analyzer")
    parser.add_argument("--file", type=str, required=True, help="Path to bank statement (PDF or CSV)")
    parser.add_argument("--output", type=str, default="reports/finance_report.xlsx", help="Output Excel report path")
    
    args = parser.parse_args()
    
    run_pipeline(args.file, args.output)       