from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.contact import ContactCreate, ContactBatchCreate, ContactUpdate, ContactOut
from app.crud.contact import get_all, get_by_id, create, update, delete, batch_create
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["联系方式"])



@router.post("/batch")
def batch_create_api(obj: ContactBatchCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return batch_create(db, obj.items)


@router.get("")
def get_all_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=ContactOut)
def get_by_id_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="未找到")
    return obj


@router.post("", response_model=ContactOut)
def create_api(obj: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create(db, obj)


@router.put("/{id}", response_model=ContactOut)
def update_api(id: int, obj: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = update(db, id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result


@router.delete("/{id}")
def delete_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not delete(db, id):
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}
