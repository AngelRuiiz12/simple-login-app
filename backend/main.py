from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import models
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

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

SECRET_KEY = "mi_clave_super_secreta_y_larga_que_nadie_debe_saber"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # El token caducará a los 30 minutos

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()

    # Calculamos cuándo expirará el token
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Creamos el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except jwt.PyJWTError:  # Si el token es inválido o caducó
        raise credentials_exception

    # Si el token es válido, buscamos al usuario en la bbdd
    stmt = select(models.User).where(models.User.email == email)
    user = db.execute(stmt).scalar()

    if user is None:
        raise credentials_exception

    return user


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ENDPOINTS
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

    token_data = {"sub": db_user.email}  # sub = subject (convención estándar)
    access_token = create_access_token(token_data)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/dashboard-data")
def read_dashboard(current_user: models.User = Depends(get_current_user)):
    return {
        "mensaje": f"¡Hola {current_user.email}! Bienvenido a tu Dashboard secreto.",
        "datos_privados": "Aquí hay gráficas y cosas súper confidenciales.",
    }


@app.get("/profile-data")
def read_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role": "Usuario Estándar",
        "mensaje": "Estos son los datos de tu perfil privado.",
    }
