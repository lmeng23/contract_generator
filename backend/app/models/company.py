from sqlalchemy import Column, Integer, String, DateTime, func, text
from app.database import Base


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50))
    address = Column(String(255))
    tax_id = Column(String(100))
    bank_account = Column(String(100))
    bank_address = Column(String(255))
    legal_person = Column(String(100))
    agent = Column(String(100))
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("(DATETIME(CURRENT_TIMESTAMP, '+8 hours'))")
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("(DATETIME(CURRENT_TIMESTAMP, '+8 hours'))"),
        onupdate=func.datetime(func.current_timestamp(), '+8 hours')
    )
