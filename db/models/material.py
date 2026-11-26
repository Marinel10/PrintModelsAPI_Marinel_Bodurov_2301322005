from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index, func

from db.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.print_model_material import PrintModelMaterial


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    print_model_materials: Mapped[list["PrintModelMaterial"]] = relationship(back_populates="material")

    __table_args__ = (
        Index( "uq_category_name_normalized",  func.lower(func.trim(name)), unique=True),
    )