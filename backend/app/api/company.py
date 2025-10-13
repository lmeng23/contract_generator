from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyInDB
from app.database import get_db
from app.core import crud_company

router = APIRouter()


@router.get("/suggest", response_model=list[CompanyInDB])
def suggest_companies(keyword: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return crud_company.suggest_companies(db, keyword)


@router.get("/{company_id}", response_model=CompanyInDB)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = crud_company.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/create", response_model=CompanyInDB)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    # 在创建之前检查公司是否已存在
    existing_company = crud_company.get_company_by_name(db, data.name)
    if existing_company:
        # 如果公司已存在，选择更新
        updated_company = crud_company.update_company(
            db, existing_company.id, data)
        return updated_company
    else:
        # 如果公司不存在，执行创建操作
        return crud_company.create_company(db, data)


@router.put("/{company_id}", response_model=CompanyInDB)
def update_company(company_id: int, data: CompanyUpdate, db: Session = Depends(get_db)):
    company = crud_company.update_company(db, company_id, data)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
