from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.villager import Villager
from app.schemas.villager import VillagerCreate, VillagerUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    q = db.query(Villager)
    if search:
        q = q.filter(Villager.name.contains(search))
    total = q.count()
    items = q.offset(skip).limit(limit).all()
    return {"items": items, "total": total}


def get_by_id(db: Session, id: int):
    return db.query(Villager).filter(Villager.id == id).first()


def create(db: Session, obj: VillagerCreate):
    db_obj = Villager(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, id: int, obj: VillagerUpdate):
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
