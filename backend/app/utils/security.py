# utils/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt", "plaintext"],
    default="bcrypt",
    deprecated=["plaintext"],    # mark plaintext as deprecated
)

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
