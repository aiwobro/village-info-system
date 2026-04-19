from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.household import Household
from app.schemas.household import HouseholdCreate, HouseholdUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100):
    # 原生SQL：查户同时拿到户主姓名和户内人数
    sql = text("""
        SELECT
            h.id, h.household_no, h.natural_village_id, h.head_id, h.address,
            h.created_at, h.updated_at,
            head.name as head_name,
            COUNT(m.id) as member_count
        FROM households h
        LEFT JOIN villagers head ON h.id = head.household_id AND head.relation_to_head = '户主'
        LEFT JOIN villagers m ON h.id = m.household_id
        GROUP BY h.id, head.name
        ORDER BY h.id
        OFFSET :skip LIMIT :limit
    """)
    rows = db.execute(sql, {"skip": skip, "limit": limit}).fetchall()

    total = db.query(Household).count()

    result = []
    for r in rows:
        result.append({
            "id": r.id,
            "household_no": r.household_no,
            "natural_village_id": r.natural_village_id,
            "head_id": r.head_id,
            "address": r.address,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
            "head_name": r.head_name,
            "member_count": r.member_count,
        })
    return {"items": result, "total": total}


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
