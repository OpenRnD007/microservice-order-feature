import os
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from configs.dependency import get_db
from .utils import authenticate_user, create_access_token, get_current_active_user, get_password_hash
from .schemas import Token
from . import crud, schemas

auth_routers = APIRouter()

@auth_routers.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.

    :param form_data: The form data that contains the username and password.
    :param db: The database session dependency.
    :return: A Token object with access token and token type.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',30))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@auth_routers.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    """
    Read the current logged-in user.

    :param current_user: The current active user obtained from the token.
    :return: The User schema of the current user.
    """
    return current_user


@auth_routers.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserInDB, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    :param user: The UserInDB schema containing the user information.
    :param db: The database session dependency.
    :return: The User schema of the created user.
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = get_password_hash(user.password)
    return crud.create_user(db=db, user=user)