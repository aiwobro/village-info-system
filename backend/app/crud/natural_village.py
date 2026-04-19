from sqlalchemy.orm import Session
from app.models.natural_village import NaturalVillage
from app.schemas.natural_village import NaturalVillageCreate, NaturalVillageUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(NaturalVillage).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int):
    return db.query(NaturalVillage).filter(NaturalVillage.id == id).first()


def create(db: Session, obj: NaturalVillageCreate):
    db_obj = NaturalVillage(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, id: int, obj: NaturalVillageUpdate):
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
