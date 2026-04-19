from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100):
    items = db.query(Contact).offset(skip).limit(limit).all()
    total = db.query(Contact).count()
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
