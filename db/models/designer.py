from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index, func

from typing import TYPE_CHECKING

from db.models.base import Base
if TYPE_CHECKING:
    from db.models.print_model import PrintModel


class Designer(Base):
    __tablename__ = "designers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    print_models: Mapped[list["PrintModel"]] = relationship(back_populates="designer")



    __table_args__ = (
        Index( "uq_category_name_normalized",  func.lower(func.trim(email)), unique=True),
    )