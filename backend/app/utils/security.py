from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import get_settings


settings = get_settings()
password_hash = PasswordHash.recommended()


# Convert a password into a secure hash.
def hash_password(password):
    return password_hash.hash(password)


# Check if the entered password matches the saved hash.
def verify_password(password, saved_hash):
    return password_hash.verify(password, saved_hash)


# Create a login token that expires after 60 minutes.
def create_token(user_id):

    expire = datetime.now(timezone.utc) + timedelta(minutes=60)

    data = {
        "sub": str(user_id),   # Example: "101"
        "exp": expire
    }

    return jwt.encode(
        data,
        settings.jwt_secret_key,
        algorithm="HS256"
    )


# Read and verify a login token.
def decode_token(token):
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=["HS256"]
    )
