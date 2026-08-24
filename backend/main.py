from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]


class UserRequest(BaseModel):
    email: str
    password: str = Field(min_length=4, max_length=50)


# CONFIGURACIÓN DE SEGURIDAD
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/register")
def register(user: UserRequest, db: SessionDep):
    stmt = select(models.User).where(models.User.email == user.email)
    db_user = db.execute(stmt).scalar()

    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = get_password_hash(user.password)

    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()

    return {"message": "Usuario creado con éxito"}


@app.post("/login")
def login(user: UserRequest, db: SessionDep):
    stmt = select(models.User).where(models.User.email == user.email)
    db_user = db.execute(stmt).scalar()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {"message": "Login exitoso!", "email": db_user.email}
