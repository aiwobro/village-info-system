from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.household import HouseholdCreate, HouseholdUpdate, HouseholdOut, HouseholdBatchCreate
from app.crud.household import get_all, get_by_id, create, update, delete, get_stats, batch_create
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/households", tags=["户管理"])


@router.get("")
def get_all_api(skip: int = 0, limit: int = 100, natural_village_id: int = Query(None), admin_village_id: int = Query(None), search: str = Query(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all(db, skip=skip, limit=limit, natural_village_id=natural_village_id, admin_village_id=admin_village_id, search=search)


@router.get("/stats")
def get_stats_api(natural_village_id: int = Query(None), admin_village_id: int = Query(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_stats(db, natural_village_id=natural_village_id, admin_village_id=admin_village_id)


@router.post("/batch")
def batch_create_api(obj: HouseholdBatchCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return batch_create(db, obj.items)


@router.get("/{id}", response_model=HouseholdOut)
def get_by_id_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="未找到")
    return obj


@router.post("", response_model=HouseholdOut)
def create_api(obj: HouseholdCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create(db, obj)


@router.put("/{id}", response_model=HouseholdOut)
def update_api(id: int, obj: HouseholdUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = update(db, id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result


@router.delete("/{id}")
def delete_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not delete(db, id):
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}
