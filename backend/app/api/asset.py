from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.asset import AssetCreate, AssetUpdate, AssetOut
from app.crud import asset as crud

router = APIRouter(prefix="/assets", tags=["资产管理"])

@router.get("", response_model=list[AssetOut])
def get_all(
    skip: int = 0,
    limit: int = 20,
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_all(db, skip=skip, limit=limit, search=search)

@router.get("/count")
def get_count(search: str = Query(None), db: Session = Depends(get_db)):
    return {"count": crud.get_count(db, search=search)}

@router.get("/{id}", response_model=AssetOut)
def get_by_id(id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="未找到")
    return obj

@router.post("", response_model=AssetOut)
def create(obj: AssetCreate, db: Session = Depends(get_db)):
    return crud.create(db, obj)

@router.put("/{id}", response_model=AssetOut)
def update(id: int, obj: AssetUpdate, db: Session = Depends(get_db)):
    result = crud.update(db, id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    if not crud.delete(db, id):
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}
