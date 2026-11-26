from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index, func

from db.models.base import Base
from db.models.print_model import PrintModel

class Category(Base):
    __tablename__ = "categories"


    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    print_models: Mapped[list["PrintModel"]] = relationship(back_populates="category")


    __table_args__ = (
        Index( "uq_category_name_normalized",  func.lower(func.trim(name)), unique=True),
    )