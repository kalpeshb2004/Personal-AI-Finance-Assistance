from src.database import SessionLocal, User, Statement, Transaction

def save_to_database(account_details, df, file_name):
    session = SessionLocal()
    
    try:
        # Step 1: User save karo (ya agar already hai to use karo)
        existing_user = session.query(User).filter_by(
            account_no=account_details.get("AccountNo")
        ).first()
        
        if existing_user:
            user = existing_user
        else:
            user = User(
                name=account_details.get("Name"),
                account_no=account_details.get("AccountNo"),
                bank_name=account_details.get("BankName"),
                branch=account_details.get("Branch"),
                ifsc=account_details.get("IFSC"),
                address=account_details.get("Address"),
            )
            session.add(user)
            session.flush()  # user.id abhi generate karwa do, commit se pehle
        
        # Step 2: Statement entry banao
        statement = Statement(
            user_id=user.id,
            file_name=file_name,
            total_transactions=len(df),
        )
        session.add(statement)
        session.flush()  # statement.id generate karwao
        
        # Step 3: Har transaction save karo
        for _, row in df.iterrows():
            txn = Transaction(
                statement_id=statement.id,
                date=row["Date"],
                description=row["Description"],
                clean_merchant=row["CleanMerchant"],
                category=row["Category"],
                withdrawal=row["Withdrawal"],
                deposit=row["Deposit"],
                balance=row["Balance"],
                match_type=row.get("MatchType", ""),
            )
            session.add(txn)
        
        session.commit()
        print(f"Saved to DB: User ID {user.id}, Statement ID {statement.id}, {len(df)} transactions")
        return statement.id
    
    except Exception as e:
        session.rollback()
        print(f"Database save error: {e}")
        raise
    finally:
        session.close()