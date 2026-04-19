from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut
from app.crud import contact as crud
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["联系方式"])

@router.get("")
def get_all(
    skip: int = 0,
    limit: int = 100,
    villager_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_all(db, skip=skip, limit=limit, villager_id=villager_id)

@router.get("/{id}", response_model=ContactOut)
def get_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = crud.get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="未找到")
    return obj

@router.post("", response_model=ContactOut)
def create(obj: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create(db, obj)

@router.put("/{id}", response_model=ContactOut)
def update(id: int, obj: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = crud.update(db, id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not crud.delete(db, id):
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}
