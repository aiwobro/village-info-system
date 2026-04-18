from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate, BankAccountOut
from app.crud import bank_account as crud

router = APIRouter(prefix="/bank-accounts", tags=["银行账号"])

@router.get("", response_model=list[BankAccountOut])
def get_all(
    skip: int = 0,
    limit: int = 100,
    villager_id: int = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_all(db, skip=skip, limit=limit, villager_id=villager_id)

@router.get("/{id}", response_model=BankAccountOut)
def get_by_id(id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="未找到")
    return obj

@router.post("", response_model=BankAccountOut)
def create(obj: BankAccountCreate, db: Session = Depends(get_db)):
    return crud.create(db, obj)

@router.put("/{id}", response_model=BankAccountOut)
def update(id: int, obj: BankAccountUpdate, db: Session = Depends(get_db)):
    result = crud.update(db, id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    if not crud.delete(db, id):
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}
