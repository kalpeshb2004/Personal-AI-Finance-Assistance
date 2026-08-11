from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from src.data_loader import load_and_clean
from src.categorizer import categorize_dataframe
from src.visualizer import plot_category_pie, plot_category_bar
from src.report_generator import generate_pdf_report
from src.pdf_parser import extract_account_details
from src.db_operations import save_to_database

app = FastAPI(title="Personal Finance Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "Finance Bot API is running"}


@app.post("/upload")
async def upload_statement(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        df = load_and_clean(file_path)
        df = categorize_dataframe(df)
        
        plot_category_pie(df)
        plot_category_bar(df)
        
        account_details = extract_account_details(file_path)
        generate_pdf_report(df, account_details)
        save_to_database(account_details, df, file.filename)
        
        spend_df = df[(df["Withdrawal"] > 0) & (df["Category"] != "Person Transfer")]
        total_spend = float(spend_df["Withdrawal"].sum())
        category_totals = spend_df.groupby("Category")["Withdrawal"].sum().to_dict()
        
        transfer_df = df[df["Category"] == "Person Transfer"]
        total_sent = float(transfer_df["Withdrawal"].sum())
        total_received = float(transfer_df["Deposit"].sum())
        
        return {
            "success": True,
            "account_details": account_details,
            "summary": {
                "total_spend": total_spend,
                "person_transfer_sent": total_sent,
                "person_transfer_received": total_received,
                "total_transactions": len(df),
            },
            "category_breakdown": category_totals,
            "transactions": df[["Date", "Description", "Category", "Withdrawal", "Deposit", "Balance"]].astype(str).to_dict(orient="records"),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))