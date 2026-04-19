from sqlalchemy.orm import Session
from app.models.admin_village import AdminVillage
from app.schemas.admin_village import AdminVillageCreate, AdminVillageUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AdminVillage).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int):
    return db.query(AdminVillage).filter(AdminVillage.id == id).first()


def create(db: Session, obj: AdminVillageCreate):
    db_obj = AdminVillage(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, id: int, obj: AdminVillageUpdate):
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
