from sqlalchemy.orm import Session
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.models.company import Company


def get_company_by_name(db: Session, name: str):
    return db.query(Company).filter(Company.name == name).first()


def suggest_companies(db: Session, keyword: str):
    return db.query(Company).filter(Company.name.like(f"%{keyword}%")).all()


def get_company(db: Session, company_id: int):
    return db.query(Company).get(company_id)


def create_company(db: Session, data: CompanyCreate):
    company = Company(**data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def update_company(db: Session, company_id: int, data: CompanyUpdate):
    company = db.query(Company).get(company_id)
    if not company:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company
