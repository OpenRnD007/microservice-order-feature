from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class User(Base):
    """
    User model for representing users in the database.

    Attributes:
    id (int): Unique identifier for the user, serves as the primary key.
    username (str): Unique username for the user, used for identification.
    password (str): Hashed password for the user, used for authentication.
    full_name (str): Full name of the user.
    is_active (bool): Flag to indicate if the user account is active. Defaults to True.
    disabled (bool): Flag to indicate if the user account is disabled. Defaults to False.
    """
    __tablename__ = "movies_users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    disabled = Column(Boolean, default=False)