from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.session import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    aadhar_card_number = Column(String(12), unique=True, index=True, nullable=False)
    mobile_number = Column(String(10), unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    account_number = Column(String(12), unique=True, index=True, nullable=False)
    account_type = Column(String, default="savings", nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    is_frozen = Column(Boolean, default=False, nullable=False)