from pydantic import BaseModel

class Token(BaseModel):
    """
    Token model that represents the access token and its type.
    """
    access_token: str # The JWT access token
    token_type: str # The type of the token (e.g., "bearer")


class TokenData(BaseModel):
    """
    TokenData model that holds the username extracted from the token payload.
    """
    username: str | None = None # The username from the token payload, optional

class User(BaseModel):
    """
    User model that represents a user in the system.
    """
    id: int | None = None # The unique ID of the user, optional
    username: str | None = None # The username of the user, optional    
    full_name: str | None = None # The full name of the user, optional
    disabled: bool | None = None # Indicates if the user is disabled, optional
    is_active: bool | None = None # Indicates if the user is active, optional

    class Config:
        from_attributes = True # Enable ORM mode for compatibility with ORMs like SQLAlchemy


class UserInDB(User):
    """
    UserInDB model that extends the User model with a password field for database records.
    """
    password: str # The hashed password of the user