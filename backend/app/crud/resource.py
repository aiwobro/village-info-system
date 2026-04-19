from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate


def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None, natural_village_id: int = None):
    query = db.query(Resource)
    if search:
        query = query.filter(
            or_(
                Resource.name.ilike(f"%{search}%"),
                Resource.code.ilike(f"%{search}%"),
            )
        )
    if natural_village_id:
        query = query.filter(Resource.natural_village_id == natural_village_id)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"items": items, "total": total}

def get_by_id(db: Session, id: int):
    return db.query(Resource).filter(Resource.id == id).first()

def create(db: Session, obj: ResourceCreate):
    db_obj = Resource(**obj.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, id: int, obj: ResourceUpdate):
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
            db_obj = Resource(**obj.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            results["success"] += 1
        except Exception as e:
            db.rollback()
            results["failed"] += 1
            results["errors"].append({"row": i + 1, "msg": str(e)})
    return results
