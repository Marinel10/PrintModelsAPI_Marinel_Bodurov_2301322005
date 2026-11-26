from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.models import Material, PrintModelMaterial
from models.material import MaterialCreate, MaterialUpdate
from exceptions import AppError, NotFound, ConflictError


class MaterialService:

    # List of Materials
    def list(self, db_session: Session) -> list[Material]:

        materials = list(db_session.scalars(select(Material)).all())

        return materials

    # Get by  ID
    def get(self, material_id: int, db_session: Session) -> Material:
        material = db_session.get(Material, material_id)

        if material is None:
            raise NotFound(f"No such material found with id='{material_id}'")

        return material

    def create(self, data: MaterialCreate, db_session: Session) -> Material:
        stmt = select(Material).where(
            func.lower(func.trim(Material.name)) == data.name.lower()
        )

        if db_session.scalars(stmt).first():
            raise ConflictError(
                f"Material with name '{data.name}' already exists"
            )

        material = Material(name=data.name)

        db_session.add(material)

        try:
            db_session.commit()

        except IntegrityError:
            db_session.rollback()

            raise ConflictError("Material violates database constraints")

        db_session.refresh(material)
        return material

    def update(self, material_id: int, data: MaterialUpdate, db_session: Session) -> Material:

        material = self.get(material_id, db_session)
        changes = data.model_dump(exclude_unset=True)

        if "name" in changes:
            if changes["name"] is None:
                raise AppError("Material name cannot be null")

            stmt = select(Material).where(
                func.lower(func.trim(Material.name)) == changes["name"].lower(),
                Material.id != material_id
            )

            if db_session.scalars(stmt).first():
                raise ConflictError(
                    f"Material with name '{changes['name']}' already exists"
                )

            material.name = changes["name"]

        try:
            db_session.commit()

        except IntegrityError:
            db_session.rollback()
            raise ConflictError("Material update violates database constraints")

        db_session.refresh(material)
        return material

    # Delete material if dosen't have model
    def delete(self, material_id: int, db_session: Session) -> int:

        material = self.get(material_id, db_session)

        stmt = select(PrintModelMaterial).where(
            PrintModelMaterial.material_id == material_id
        )

        if db_session.scalars(stmt).first():
            raise ConflictError("The Material is used by print models!")

        db_session.delete(material)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise ConflictError("Cannot delete material in use")

        return material_id
