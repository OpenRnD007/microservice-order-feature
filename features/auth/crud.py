from sqlalchemy.orm import Session
#from auth.utils import get_password_hash

from . import models, schemas


def get_user(db: Session, user_id: int):
    """
    Retrieve a user from the database by their user ID.

    :param db: The database session.
    :param user_id: The unique ID of the user.
    :return: The User model instance if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user from the database by their username.

    :param db: The database session.
    :param username: The username of the user.
    :return: The User model instance if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def validate_user(db: Session, username: str, password: str):
    """
    Validate a user's credentials.

    :param db: The database session.
    :param username: The username of the user.
    :param password: The password of the user.
    :return: The User model instance if credentials are valid, otherwise None.
    """
    return db.query(models.User).filter(models.User.username == username, models.User.password == password).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of users from the database, with optional pagination.

    :param db: The database session.
    :param skip: The number of records to skip (for pagination).
    :param limit: The maximum number of records to return (for pagination).
    :return: A list of User model instances.
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserInDB):
    """
    Create a new user in the database.

    :param db: The database session.
    :param user: The UserInDB schema containing the user information.
    :return: The newly created User model instance.
    """
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user