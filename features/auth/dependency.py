from .database import SessionLocal

async def get_db():
    """
    Dependency that creates a new database session for each request.

    Yields a database session that is used in path operations that require a database connection.
    After the request is finished, the session is closed.

    :yield: An instance of the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()