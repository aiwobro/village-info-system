from sqlalchemy.orm import Session
from app.models.village import Village
from app.schemas.village import VillageCreate, VillageUpdate

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Village).offset(skip).limit(limit).all()

def get_by_id(db: Session, id: int):
    return db.query(Village).filter(Village.id == id).first()

def create(db: Session, obj: VillageCreate):
    db_obj = Village(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, id: int, obj: VillageUpdate):
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
