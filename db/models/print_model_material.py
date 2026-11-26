from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.print_model import PrintModel
    from db.models.material import Material


class PrintModelMaterial(Base):
    __tablename__ = "print_model_materials"

    print_model_id: Mapped[int] = mapped_column(
        ForeignKey("print_models.id", ondelete="CASCADE")
        ,primary_key=True
    )

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id", ondelete="RESTRICT"),
        primary_key=True
    )

    quantity: Mapped[float]
    unit: Mapped[str]

    print_model: Mapped["PrintModel"] = relationship(back_populates="print_model_materials")

    material: Mapped["Material"] = relationship(back_populates="print_model_materials")


    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_quantity_positive"),
        CheckConstraint("unit IN ('g', 'm', 'ml')", name="ck_material_unit"),
    )
