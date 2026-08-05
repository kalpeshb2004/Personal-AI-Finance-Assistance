import pdfplumber
import pandas as pd
import re

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

#extracting accounts details
def extract_account_details(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page_text = pdf.pages[0].extract_text()
    
    lines = first_page_text.split("\n")  # Poore text ko line-by-line list banao
    details = {}
    
    # Name + Account No (same line pe hain)
    name_match = re.search(r'([A-Za-z\s]+?)\s+Account No\.\s*(\d+)', first_page_text)
    details["Name"] = name_match.group(1).strip() if name_match else "Not Found"
    details["AccountNo"] = name_match.group(2) if name_match else "Not Found"
    
    # IFSC
    ifsc_match = re.search(r'IFSC Code\s*([A-Z0-9]+)', first_page_text)
    details["IFSC"] = ifsc_match.group(1) if ifsc_match else "Not Found"
    
    # Bank Name — IFSC prefix se
    ifsc_bank_map = {
        "KKBK": "Kotak Mahindra Bank",
        "HDFC": "HDFC Bank",
        "ICIC": "ICICI Bank",
        "SBIN": "State Bank of India",
        "UTIB": "Axis Bank",
        "PUNB": "Punjab National Bank",
    }
    ifsc_prefix = details["IFSC"][:4] if details["IFSC"] != "Not Found" else ""
    details["BankName"] = ifsc_bank_map.get(ifsc_prefix, "Unknown Bank")
    
    # Ab har line ko individually check karo — sirf exact single line ka content lo
    address_parts = []
    branch = "Not Found"
    
    for line in lines:
        line = line.strip()
        if line.startswith("Branch "):
            branch = line.replace("Branch", "", 1).strip()
        elif line.startswith("Plot No"):
            address_parts.append(line)
        elif "Colony" in line:
            address_parts.append(line)
        elif "Apartment" in line:
            address_parts.append(line)
        elif re.match(r'^[A-Za-z]+\s*-\s*\d{6}', line):  # City - Pincode pattern
            city_pin = re.match(r'^([A-Za-z]+\s*-\s*\d{6})', line)
            address_parts.append(city_pin.group(1))
        elif re.match(r'^[A-Za-z]+\s*-\s*India', line):
            address_parts.append(line.strip())
    
    details["Branch"] = branch
    details["Address"] = ", ".join(address_parts) if address_parts else "Not Found"
    
    return details

if __name__ == "__main__":
    import pdfplumber
    with pdfplumber.open("data/AccountStatement_01-Aug-2026_03-Aug-2026.pdf") as pdf:
        text = pdf.pages[0].extract_text()
        print(repr(text))


