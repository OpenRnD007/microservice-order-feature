from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext # type: ignore
from datetime import datetime, timedelta, timezone
import jwt
import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from configs.dependency import get_db
from . import crud
from .schemas import TokenData, User

# Define the token URL for obtaining tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define the password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Verify a password against a given hashed password.

    :param plain_password: The plaintext password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hash a password using bcrypt.

    :param password: The plaintext password to hash.
    :return: The hashed password.
    """
    return pwd_context.hash(password)

def authenticate_user(db, username: str, password: str):
    """
    Authenticate a user by username and password.

    :param db: The database session.
    :param username: The username of the user.
    :param password: The plaintext password of the user.
    :return: The User object if authentication is successful, False otherwise.
    """
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.

    :param data: The data to encode in the token.
    :param expires_delta: The timedelta for token expiration (default is 15 minutes).
    :return: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, 
                             os.getenv('SECRET_KEY', 'a8c78182ee3e4122d0ffe62784ba7a403d874de11e538abd475fe91ca0542658'), 
                             algorithm=os.getenv('ALGORITHM','HS256'))
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
    Retrieve the current user based on the token.

    :param token: The JWT token.
    :param db: The database session.
    :return: The User object if the token is valid, raises an HTTPException otherwise.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, 
                             os.getenv('SECRET_KEY', 'a8c78182ee3e4122d0ffe62784ba7a403d874de11e538abd475fe91ca0542658'), 
                             algorithms=[os.getenv('ALGORITHM','HS256')])
        username: str = payload.get("sub")
        #print(payload)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Retrieve the current active user.

    :param current_user: The User object obtained from the token.
    :return: The User object if the user is active, raises an HTTPException if the user is inactive.
    """
    if current_user and current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
