from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.models import Designer, PrintModel
from models.designer import DesignerCreate, DesignerUpdate

from exceptions import AppError, NotFound, ConflictError


class DesignerService:

    # List of Designers
    def list(self, db_session: Session) -> list[Designer]:

        stmt = select(Designer)
        designers = list(db_session.scalars(stmt).all())

        return designers

    # By ID
    def get(self, designer_id: int, db_session: Session) -> Designer:

        designer = db_session.get(Designer, designer_id)

        if designer is None:
            raise NotFound(f"No such designer found with id='{designer_id}'")


        return designer


    def create(self, data: DesignerCreate, db_session: Session) -> Designer:

        email = str(data.email).strip().lower()

        stmt = select(Designer).where(
            func.lower(func.trim(Designer.email)) == email
        )

        is_designer_exists = db_session.scalars(stmt).first()

        if is_designer_exists:
            raise ConflictError(f"Designer with email '{email}' already exists")

        designer = Designer(name=data.name, email=email)

        db_session.add(designer)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise ConflictError("Designer with this email already exists")

        db_session.refresh(designer)
        return designer


    def update(self,designer_id: int,data: DesignerUpdate,db_session: Session) -> Designer:

        designer = self.get(designer_id, db_session)
        changes = data.model_dump(exclude_unset=True)

        if "name" in changes:
            if changes["name"] is None:
                raise AppError("Designer name cannot be null")

            designer.name = changes["name"]

        if "email" in changes:
            if changes["email"] is None:
                raise AppError("Designer email cannot be null")

            email = str(changes["email"]).strip().lower()

            stmt = select(Designer).where(
                func.lower(func.trim(Designer.email)) == email,
                Designer.id != designer_id
            )

            designer_exists = db_session.scalars(stmt).first()

            if designer_exists:
                raise ConflictError(f"Designer with email '{email}' already exists")

            designer.email = email

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise ConflictError("Designer update violates database constraints")

        db_session.refresh(designer)
        return designer

    # Delete Designer if dosen't have 3D model
    def delete(self, designer_id: int, db_session: Session) -> int:
        designer = self.get(designer_id, db_session)

        stmt = select(PrintModel).where(
            PrintModel.designer_id == designer_id
        )

        designer_have_model = db_session.scalars(stmt).first()

        if designer_have_model:
            raise ConflictError("The Designer has print models!")

        db_session.delete(designer)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise ConflictError("Cannot delete designer with print models")

        return designer_id
