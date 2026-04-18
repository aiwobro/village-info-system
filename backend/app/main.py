from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models import Village, Villager, Contact, BankAccount, Asset, Resource
from app.models.user import User
from app.api import village, villager, contact, bank_account, asset, resource
from app.api.auth import router as auth_router

# Create tables
Base.metadata.create_all(bind=engine)

# Create default admin user if not exists
def create_default_admin():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "admin").first()
        if not user:
            from app.core.security import get_password_hash
            admin = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="系统管理员"
            )
            db.add(admin)
            db.commit()
            print("Default admin user created: admin / admin123")
    finally:
        db.close()

create_default_admin()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health
@app.get("/health")
def health():
    return {"status": "ok"}

# Include routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(village.router, prefix=settings.API_V1_STR)
app.include_router(villager.router, prefix=settings.API_V1_STR)
app.include_router(contact.router, prefix=settings.API_V1_STR)
app.include_router(bank_account.router, prefix=settings.API_V1_STR)
app.include_router(asset.router, prefix=settings.API_V1_STR)
app.include_router(resource.router, prefix=settings.API_V1_STR)
