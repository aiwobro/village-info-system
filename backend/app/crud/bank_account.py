from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.bank_account import BankAccount
from app.models.villager import Villager
from app.models.household import Household
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100, villager_id: int | None = None, search: str = None, natural_village_id: int = None):
    query = db.query(BankAccount).join(Villager, BankAccount.villager_id == Villager.id).join(Household, Villager.household_id == Household.id)
    if villager_id is not None:
        query = query.filter(BankAccount.villager_id == villager_id)
    if search:
        query = query.filter(or_(
            BankAccount.account_number_encrypted.contains(search),
            BankAccount.bank_name.contains(search),
            BankAccount.remark.contains(search),
            Villager.name.contains(search)
        ))
    if natural_village_id:
        query = query.filter(Household.natural_village_id == natural_village_id)
    items = query.offset(skip).limit(limit).all()
    total = query.count()
    return {"items": items, "total": total}


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


def batch_create(db: Session, items: list):
    """批量创建记录"""
    results = {"success": 0, "failed": 0, "errors": []}
    for i, obj in enumerate(items):
        try:
            db_obj = BankAccount(**obj.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            results["success"] += 1
        except Exception as e:
            db.rollback()
            results["failed"] += 1
            results["errors"].append({"row": i + 1, "msg": str(e)})
    return results
