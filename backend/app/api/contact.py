from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.contact import ContactCreate, ContactBatchCreate, ContactUpdate, ContactOut
from app.crud.contact import get_all, get_by_id, create, update, delete, batch_create, lock, unlock
from app.models.user import User
from app.api.auth import get_current_user, require_admin

router = APIRouter(prefix="/contacts", tags=["联系方式"])



@router.post("/batch")
def batch_create_api(obj: ContactBatchCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return batch_create(db, obj.items)


@router.get("")
def get_all_api(skip: int = 0, limit: int = 100, villager_id: int | None = None, search: str | None = None, natural_village_id: int | None = None, is_locked: int = Query(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all(db, skip=skip, limit=limit, villager_id=villager_id, search=search, natural_village_id=natural_village_id, is_locked=is_locked)


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
    if result == "LOCKED":
        raise HTTPException(status_code=403, detail="该记录已锁定，无法编辑")
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return result


@router.delete("/{id}")
def delete_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = delete(db, id)
    if result == "LOCKED":
        raise HTTPException(status_code=403, detail="该记录已锁定，无法删除")
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    return {"message": "删除成功"}


@router.post("/{id}/lock")
def lock_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    result = lock(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    if result == "LOCKED":
        return {"message": "该记录已是锁定状态"}
    return {"message": "锁定成功"}


@router.post("/{id}/unlock")
def unlock_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    result = unlock(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="未找到")
    if result == "NOT_LOCKED":
        return {"message": "该记录已是解锁状态"}
    return {"message": "解锁成功"}
