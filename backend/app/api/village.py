from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.village import VillageCreate, VillageUpdate, VillageOut
from app.crud import village as crud
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/villages", tags=["村庄管理"])

@router.get("")
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_all(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=VillageOut)
def get_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = crud.get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="未找到")
    return obj

@router.post("", response_model=VillageOut)
def create(obj: VillageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create(db, obj)

@router.put("/{id}", response_model=VillageOut)
def update(id: int, obj: VillageUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = crud.update(db, id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not crud.delete(db, id):
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}
