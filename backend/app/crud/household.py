from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.household import Household
from app.schemas.household import HouseholdCreate, HouseholdUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100, natural_village_id: int = None, admin_village_id: int = None, search: str = None, is_locked: int = None):
    # 动态WHERE条件
    where = ""
    params: dict = {"skip": skip, "limit": limit}
    if natural_village_id:
        where += " AND h.natural_village_id = :natural_village_id"
        params["natural_village_id"] = natural_village_id
    if admin_village_id:
        where += " AND nv.admin_village_id = :admin_village_id"
        params["admin_village_id"] = admin_village_id
    if search:
        where += " AND h.id IN (SELECT household_id FROM villagers WHERE (name ILIKE :search OR id_card ILIKE :search) AND household_id IS NOT NULL)"
        params["search"] = f"%{search}%"
    if is_locked is not None:
        where += " AND h.is_locked = :is_locked"
        params["is_locked"] = is_locked

    sql = text(f"""
        SELECT
            h.id, h.household_no, h.natural_village_id, h.head_id, h.address, h.is_locked,
            h.created_at, h.updated_at,
            head.name as head_name,
            COUNT(m.id) as member_count
        FROM households h
        LEFT JOIN natural_villages nv ON h.natural_village_id = nv.id
        LEFT JOIN villagers head ON h.id = head.household_id AND head.relation_to_head = '户主'
        LEFT JOIN villagers m ON h.id = m.household_id
        WHERE 1=1 {where}
        GROUP BY h.id, head.name
        ORDER BY h.id
        OFFSET :skip LIMIT :limit
    """)
    rows = db.execute(sql, params).fetchall()

    # total也要带筛选条件
    count_sql = text(f"""
        SELECT COUNT(*) FROM households h
        LEFT JOIN natural_villages nv ON h.natural_village_id = nv.id
        LEFT JOIN villagers head ON h.id = head.household_id AND head.relation_to_head = '户主'
        WHERE 1=1 {where}
    """)
    total = db.execute(count_sql, {k: v for k, v in params.items() if k in ("natural_village_id", "admin_village_id", "search", "is_locked")}).scalar()

    result = []
    for r in rows:
        result.append({
            "id": r.id,
            "household_no": r.household_no,
            "natural_village_id": r.natural_village_id,
            "head_id": r.head_id,
            "address": r.address,
            "is_locked": r.is_locked,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
            "head_name": r.head_name,
            "member_count": r.member_count,
        })
    return {"items": result, "total": total}


def get_stats(db: Session, natural_village_id: int = None, admin_village_id: int = None):
    """返回当前筛选条件下的户数和总人数"""
    where = ""
    params: dict = {}
    if natural_village_id:
        where += " AND h.natural_village_id = :natural_village_id"
        params["natural_village_id"] = natural_village_id
    if admin_village_id:
        where += " AND nv.admin_village_id = :admin_village_id"
        params["admin_village_id"] = admin_village_id

    household_count = db.execute(text(f"""
        SELECT COUNT(*) FROM households h
        LEFT JOIN natural_villages nv ON h.natural_village_id = nv.id
        WHERE 1=1 {where}
    """), params).scalar()

    villager_count = db.execute(text(f"""
        SELECT COUNT(*) FROM villagers v
        LEFT JOIN households h ON v.household_id = h.id
        LEFT JOIN natural_villages nv ON h.natural_village_id = nv.id
        WHERE v.household_id IS NOT NULL AND 1=1 {where}
    """), params).scalar()

    return {"household_count": household_count or 0, "villager_count": villager_count or 0}


def get_by_id(db: Session, id: int):
    return db.query(Household).filter(Household.id == id).first()


def lock(db: Session, id: int):
    """锁定记录，已锁定返回 "LOCKED"，不存在返回 None，成功返回对象"""
    db_obj = get_by_id(db, id)
    if not db_obj:
        return None
    if db_obj.is_locked:
        return "LOCKED"
    db_obj.is_locked = 1
    db.commit()
    db.refresh(db_obj)
    return db_obj


def unlock(db: Session, id: int):
    """解锁记录，未锁定返回 "NOT_LOCKED"，不存在返回 None，成功返回对象"""
    db_obj = get_by_id(db, id)
    if not db_obj:
        return None
    if not db_obj.is_locked:
        return "NOT_LOCKED"
    db_obj.is_locked = 0
    db.commit()
    db.refresh(db_obj)
    return db_obj


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


def batch_create(db: Session, items: list):
    """批量创建户记录"""
    results = {"success": 0, "failed": 0, "errors": []}
    for i, obj in enumerate(items):
        try:
            db_obj = Household(**obj.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            results["success"] += 1
        except Exception as e:
            db.rollback()
            results["failed"] += 1
            results["errors"].append({"row": i + 1, "msg": str(e)})
    return results
