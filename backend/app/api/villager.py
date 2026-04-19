from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.villager import VillagerCreate, VillagerUpdate, VillagerOut
from app.crud import villager as crud
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/villagers", tags=["村民管理"])

@router.get("")
def get_all(
    skip: int = 0,
    limit: int = 20,
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_all(db, skip=skip, limit=limit, search=search)

@router.get("/count")
def get_count(search: str = Query(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"count": crud.get_count(db, search=search)}

@router.get("/{id}", response_model=VillagerOut)
def get_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = crud.get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="未找到")
    return obj

@router.post("", response_model=VillagerOut)
def create(obj: VillagerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create(db, obj)

@router.put("/{id}", response_model=VillagerOut)
def update(id: int, obj: VillagerUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = crud.update(db, id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not crud.delete(db, id):
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}
