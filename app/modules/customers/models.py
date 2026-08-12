from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from sqlalchemy.sql import func

class Customer(Base):
    """
    Database model for the Customer entity.
    """

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    national_id: Mapped[str] = mapped_column(String(10), unique=True,index = True, nullable=False)

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)

    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),nullable=False,)