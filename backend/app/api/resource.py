from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.resource import ResourceCreate, ResourceBatchCreate, ResourceUpdate, ResourceOut
from app.crud import resource as crud
from app.crud.resource import lock as resource_lock, unlock as resource_unlock
from app.models.user import User
from app.api.auth import get_current_user, require_admin

router = APIRouter(prefix="/resources", tags=["资源管理"])


@router.post("/batch")
def batch_create_api(obj: ResourceBatchCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return batch_create(db, obj.items)


@router.get("")
def get_all(
    skip: int = 0,
    limit: int = 20,
    search: str = Query(None),
    natural_village_id: int = Query(None),
    is_locked: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_all(db, skip=skip, limit=limit, search=search, natural_village_id=natural_village_id, is_locked=is_locked)

@router.get("/{id}", response_model=ResourceOut)
def get_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    obj = crud.get_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="未找到")
    return obj

@router.post("", response_model=ResourceOut)
def create(obj: ResourceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create(db, obj)

@router.put("/{id}", response_model=ResourceOut)
def update(id: int, obj: ResourceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = crud.update(db, id, obj)
    if result == "LOCKED":
        raise HTTPException(status_code=403, detail="该记录已锁定，无法编辑")
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = crud.delete(db, id)
    if result == "LOCKED":
        raise HTTPException(status_code=403, detail="该记录已锁定，无法删除")
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}

@router.post("/{id}/lock")
def lock_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    result = resource_lock(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    if result == "LOCKED":
        return {"message": "该记录已是锁定状态"}
    return {"message": "锁定成功"}

@router.post("/{id}/unlock")
def unlock_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    result = resource_unlock(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    if result == "NOT_LOCKED":
        return {"message": "该记录已是解锁状态"}
    return {"message": "解锁成功"}
