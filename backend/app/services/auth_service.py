from sqlalchemy import select

from app.db.models import User
from app.utils.security import hash_password, verify_password


# Find a user by email.
def find_user(db, email):
    return db.scalar(
        select(User).where(User.email == email)
    )


# Register a new user in PostgreSQL.
def register_user(db, email, password):

    user = User(
        email=email,
        password_hash=hash_password(password),
        role="engineer"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# Check whether the login details are correct.
def check_login(db, email, password):

    user = find_user(db, email)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
