from pydantic import BaseModel
from typing import Optional


class CompanyBase(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    bank_account: Optional[str] = None
    bank_address: Optional[str] = None
    legal_person: Optional[str] = None
    agent: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyInDB(CompanyBase):
    id: int

    class Config:
        orm_mode = True
