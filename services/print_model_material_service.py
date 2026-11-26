from __future__ import annotations


from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.models import PrintModel, Material, PrintModelMaterial
from models.print_model_material import (
    PrintModelMaterialRead,
    PrintModelMaterialCreate,
    PrintModelMaterialUpdate
)
from exceptions import AppError, NotFound, ConflictError


class PrintModelMaterialService:

    # All materials for 3D model
    def list(self, print_model_id: int, db_session: Session) -> list[PrintModelMaterial]:

        print_model = db_session.get(PrintModel, print_model_id)

        if print_model is None:
            raise NotFound("Print model not found")

        stmt = select(PrintModelMaterial).where(
            PrintModelMaterial.print_model_id == print_model_id
        )

        print_model_materials =list(db_session.execute(stmt).scalars().all())

        return print_model_materials

    # Add material to 3D model
    def create(self, print_model_id: int, data: PrintModelMaterialCreate, db_session: Session
    ) -> PrintModelMaterial:

        is_print_model = db_session.get(PrintModel, print_model_id)

        is_material = db_session.get(Material, data.material_id)

        # Dose model exist ?
        if is_print_model is None:
            raise NotFound("Print model not found")

        # Dose material exist ?

        if is_material is None:
            raise NotFound("Material not found")

        # Dose model have this material
        association = db_session.get(
            PrintModelMaterial,
            (print_model_id, data.material_id)
        )

        if association is not None:
            raise ConflictError(
                "Material is already added to this print model"
            )

        association = PrintModelMaterial(
            print_model_id=print_model_id,
            material_id=data.material_id,
            quantity=data.quantity,
            unit=data.unit.value
        )

        db_session.add(association)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise ConflictError("Cannot add material to print model")

        db_session.refresh(association)
        return association

    #  Upddate unit or quantity
    def update(self, print_model_id: int, material_id: int, data: PrintModelMaterialUpdate, db_session: Session
    ) -> PrintModelMaterial:

        if db_session.get(PrintModel, print_model_id) is None:
            raise NotFound("Print model not found")

        association = db_session.get(
            PrintModelMaterial,
            (print_model_id, material_id)
        )

        if association is None:
            raise NotFound("Material association not found")

        changes = data.model_dump(exclude_unset=True)

        for field, value in changes.items():
            if value is None:
                raise AppError(f"{field} cannot be null")

            if field == "unit":
                value = value.value

            setattr(association, field, value)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise ConflictError("Cannot update material association")

        db_session.refresh(association)
        return association

    # Remove material from Model
    def delete(self, print_model_id: int, material_id: int, db_session: Session) -> int:

        if db_session.get(PrintModel, print_model_id) is None:
            raise NotFound("Print model not found")

        association = db_session.get(
            PrintModelMaterial,
            (print_model_id, material_id)
        )

        if association is None:
            raise NotFound("Material association not found")

        db_session.delete(association)
        db_session.commit()

        return material_id

    # Recalculate materials for copies of model
    # Don't make change in Db
    def recalculate(self, print_model_id: int, copies: int, db_session: Session) -> dict:

        print_model = db_session.get(PrintModel, print_model_id)

        if print_model is None:
            raise NotFound("Print model not found")

        # 50 + 05 = 55 ( ФН: 2301322005)
        if copies < 1 or copies > 55:
            raise AppError("Copies must be between 1 and 55")

        materials = self.list(print_model_id, db_session)

        result = []

        for material in materials:
            new_quantity = material.quantity * copies

            result.append({
                "material_id": material.material_id,
                "quantity": new_quantity,
                "unit": material.unit
            })

        return {
            "id": print_model.id,
            "name": print_model.name,
            "instructions": print_model.instructions,
            "print_time_minutes": print_model.print_time_minutes,
            "copies": copies,
            "designer_id": print_model.designer_id,
            "category_id": print_model.category_id,
            "materials": result
        }
