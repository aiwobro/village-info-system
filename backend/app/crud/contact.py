from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models.contact import Contact
from app.models.villager import Villager
from app.schemas.contact import ContactCreate, ContactUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100, villager_id: int | None = None, search: str = None):
    query = db.query(Contact).join(Villager, Contact.villager_id == Villager.id)
    if villager_id is not None:
        query = query.filter(Contact.villager_id == villager_id)
    if search:
        query = query.filter(or_(
            Contact.value.contains(search),
            Contact.remark.contains(search),
            Villager.name.contains(search)
        ))
    items = query.offset(skip).limit(limit).all()
    total = query.count()
    return {"items": items, "total": total}


def get_by_id(db: Session, id: int):
    return db.query(Contact).filter(Contact.id == id).first()


def create(db: Session, obj: ContactCreate):
    db_obj = Contact(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, id: int, obj: ContactUpdate):
    db_obj = get_by_id(db, id)
    if not db_obj:
        return None
    for key, value in obj.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, id: int):
    db_obj = get_by_id(db, id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True


def batch_create(db: Session, items: list):
    """批量创建记录"""
    results = {"success": 0, "failed": 0, "errors": []}
    for i, obj in enumerate(items):
        try:
            db_obj = Contact(**obj.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            results["success"] += 1
        except Exception as e:
            db.rollback()
            results["failed"] += 1
            results["errors"].append({"row": i + 1, "msg": str(e)})
    return results
