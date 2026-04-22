from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models.villager import Villager
from app.models.household import Household
from app.models.natural_village import NaturalVillage
from app.schemas.villager import VillagerCreate, VillagerUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None, household_id: int = None, natural_village_id: int = None, is_locked: int = None):
    q = db.query(Villager).join(Household, Villager.household_id == Household.id).join(NaturalVillage, Household.natural_village_id == NaturalVillage.id)
    if search:
        q = q.filter(or_(
            Villager.name.contains(search),
            Villager.id_card.contains(search)
        ))
    if household_id:
        q = q.filter(Villager.household_id == household_id)
    if natural_village_id:
        q = q.filter(Household.natural_village_id == natural_village_id)
    if is_locked is not None:
        q = q.filter(Villager.is_locked == is_locked)
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
    if db_obj.is_locked:
        return "LOCKED"
    for key, value in obj.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, id: int):
    db_obj = get_by_id(db, id)
    if not db_obj:
        return False
    if db_obj.is_locked:
        return "LOCKED"
    db.delete(db_obj)
    db.commit()
    return True


def lock(db: Session, id: int):
    """锁定村民，禁止更新和删除"""
    db_obj = get_by_id(db, id)
    if not db_obj:
        return None
    db_obj.is_locked = 1
    db.commit()
    db.refresh(db_obj)
    return db_obj


def unlock(db: Session, id: int):
    """解锁村民，允许更新和删除"""
    db_obj = get_by_id(db, id)
    if not db_obj:
        return None
    db_obj.is_locked = 0
    db.commit()
    db.refresh(db_obj)
    return db_obj


def batch_create(db: Session, items: list):
    """批量创建记录"""
    results = {"success": 0, "failed": 0, "errors": []}
    for i, obj in enumerate(items):
        try:
            db_obj = Villager(**obj.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            results["success"] += 1
        except Exception as e:
            db.rollback()
            results["failed"] += 1
            results["errors"].append({"row": i + 1, "msg": str(e)})
    return results
