from pydantic import BaseModel # type: ignore
from typing import Any, Dict

class Order(BaseModel):
    id: int
    products: Dict[str, Any] | None = None
    subtotal: int | None = None
    total: int | None = None
    discount: int | None = None
    iscanceled: bool | None = None
    user_id: int

    class Config:
        from_attributes = True # Enable ORM mode for compatibility with ORMs like SQLAlchemy