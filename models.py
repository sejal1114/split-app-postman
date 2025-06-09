from sqlalchemy import Column, Integer, String, Float
from database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    paid_by = Column(String, nullable=False)
