from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.natural_village import NaturalVillageCreate, NaturalVillageUpdate, NaturalVillageOut
from app.crud.natural_village import get_all, get_by_id, create, update, delete
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/natural-villages", tags=["自然村"])


@router.get("")
def get_all_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=NaturalVillageOut)
def get_by_id_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="未找到")
    return obj


@router.post("", response_model=NaturalVillageOut)
def create_api(obj: NaturalVillageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create(db, obj)


@router.put("/{id}", response_model=NaturalVillageOut)
def update_api(id: int, obj: NaturalVillageUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = update(db, id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result


@router.delete("/{id}")
def delete_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not delete(db, id):
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}
