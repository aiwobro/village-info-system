from sqlalchemy.orm import Session
from app.models.bank_account import BankAccount
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BankAccount).offset(skip).limit(limit).all()


def get_by_id(db: Session, id: int):
    return db.query(BankAccount).filter(BankAccount.id == id).first()


def create(db: Session, obj: BankAccountCreate):
    db_obj = BankAccount(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, id: int, obj: BankAccountUpdate):
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
