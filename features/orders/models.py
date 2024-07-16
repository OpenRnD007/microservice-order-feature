from sqlalchemy import Boolean, Column, Integer, JSON, ForeignKey
from configs.database import Base

class Order(Base):
    __tablename__ = "movies_order"

    id = Column(Integer, primary_key=True)
    products = Column(JSON)
    subtotal = Column(Integer)
    total = Column(Integer)
    discount = Column(Integer, default=0)
    iscanceled = Column(Boolean, default=False)

    # Foreign key that references the id column of the User table
    user_id = Column(Integer, ForeignKey('movies_users.id'))