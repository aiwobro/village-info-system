from sqlalchemy.orm import Session
from app.models.household import Household
from app.schemas.household import HouseholdCreate, HouseholdUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Household).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int):
    return db.query(Household).filter(Household.id == id).first()


def create(db: Session, obj: HouseholdCreate):
    db_obj = Household(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, id: int, obj: HouseholdUpdate):
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
