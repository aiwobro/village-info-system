from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate

def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Asset)
    if search:
        query = query.filter(
            or_(
                Asset.name.ilike(f"%{search}%"),
                Asset.code.ilike(f"%{search}%"),
            )
        )
    return query.offset(skip).limit(limit).all()

def get_count(db: Session, search: str = None):
    query = db.query(Asset)
    if search:
        query = query.filter(
            or_(Asset.name.ilike(f"%{search}%"), Asset.code.ilike(f"%{search}%"))
        )
    return query.count()

def get_by_id(db: Session, id: int):
    return db.query(Asset).filter(Asset.id == id).first()

def create(db: Session, obj: AssetCreate):
    db_obj = Asset(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, id: int, obj: AssetUpdate):
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
