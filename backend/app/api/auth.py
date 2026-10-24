import jwt

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.db.models import User
from app.services.auth_service import (
    find_user, register_user, check_login
)
from app.utils.security import create_token, decode_token


router = APIRouter(prefix="/auth", tags=["Authentication"])
bearer = HTTPBearer()


# Describe the information required for signup.
class SignupData(BaseModel):
    email: EmailStr                 # Example: engineer@gmail.com
    password: str = Field(min_length=8, max_length=128)


# Describe the information required for login.
class LoginData(BaseModel):
    email: EmailStr
    password: str


# Register a new user.
@router.post("/signup", status_code=201)
def signup(data: SignupData, db: Session = Depends(get_db)):

    email = str(data.email).lower()

    if find_user(db, email):
        raise HTTPException(409, "Email already registered")

    try:
        user = register_user(db, email, data.password)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Email already registered")

    return {
        "id": user.id,
        "email": user.email,
        "message": "Account created successfully"
    }


# Check login details and return an access token.
@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):

    email = str(data.email).lower()
    user = check_login(db, email, data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Identify the user from their login token.
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):

    try:
        data = decode_token(credentials.credentials)
        user_id = int(data["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError, TypeError):
        raise HTTPException(401, "Invalid or expired token")

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(401, "User not found")

    return user


# Return details of the logged-in user.
@router.get("/me")
def my_profile(user: User = Depends(get_current_user)):

    return {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }
