import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# URL.create() automatically special characters (@, #, etc.) ko safely encode karta hai
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------- TABLES ----------

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    account_no = Column(String(50))
    bank_name = Column(String(100))
    branch = Column(String(255))
    ifsc = Column(String(20))
    address = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    statements = relationship("Statement", back_populates="user")


class Statement(Base):
    __tablename__ = "statements"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_name = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    total_transactions = Column(Integer)
    
    user = relationship("User", back_populates="statements")
    transactions = relationship("Transaction", back_populates="statement")


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    statement_id = Column(Integer, ForeignKey("statements.id"))
    date = Column(DateTime)
    description = Column(String(500))
    clean_merchant = Column(String(255))
    category = Column(String(100))
    withdrawal = Column(Float)
    deposit = Column(Float)
    balance = Column(Float)
    match_type = Column(String(50))
    
    statement = relationship("Statement", back_populates="transactions")


# ---------- CREATE TABLES ----------

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    init_db()