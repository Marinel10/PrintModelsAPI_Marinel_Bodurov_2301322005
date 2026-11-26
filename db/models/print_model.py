from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.designer import Designer
    from db.models.category import Category
    from db.models.print_model_material import PrintModelMaterial


class PrintModel(Base):
    __tablename__ = "print_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    instructions: Mapped[str]
    print_time_minutes: Mapped[int]
    copies: Mapped[int]

    difficulty: Mapped[str] = mapped_column(nullable=False,server_default="medium")

    designer_id: Mapped[int] = mapped_column(
        ForeignKey("designers.id", ondelete="RESTRICT")
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL")
    )

    designer: Mapped["Designer"] = relationship(back_populates="print_models")

    category: Mapped["Category | None"] = relationship(back_populates="print_models")

    print_model_materials: Mapped[list["PrintModelMaterial"]] = relationship(back_populates="print_model",
        cascade="all, delete-orphan"
    )


    __table_args__ = (
        CheckConstraint("copies > 0",name="ck_copies_positive"),
        CheckConstraint("print_time_minutes > 0",name="ck_print_time_positive"),
        CheckConstraint("difficulty IN ('easy', 'medium', 'hard')", name="ck_print_models_difficulty")
    )
