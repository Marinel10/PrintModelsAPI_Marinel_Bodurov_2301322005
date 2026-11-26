from __future__ import annotations


from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.models import PrintModel, Designer, Category
from models.print_model import PrintModelCreate, PrintModelUpdate
from exceptions import AppError, NotFound, ConflictError


class PrintModelService:

    # Връща всички 3D модели
    def list(self, db_session: Session) -> list[PrintModel]:

        print_models = list(db_session.scalars(select(PrintModel)).all())

        return print_models

    # Търси 3D модел по ID
    def get(self, print_model_id: int, db_session: Session) -> PrintModel:
        print_model = db_session.get(PrintModel, print_model_id)

        if print_model is None:
            raise NotFound(
                f"No such print model found with id='{print_model_id}'"
            )

        return print_model

    # Създава нов 3D модел
    def create(self,data: PrintModelCreate,db_session: Session) -> PrintModel:

        designer = db_session.get(Designer, data.designer_id)

        # Проверяваме дали дизайнерът съществува
        if designer is None:
            raise NotFound("Designer not found")

        # Проверяваме категорията, ако е подадена
        if data.category_id is not None:
            if db_session.get(Category, data.category_id) is None:
                raise NotFound("Category not found")

        # Проверяваме дали дизайнерът вече има модел със същото име
        stmt = select(PrintModel).where(
            PrintModel.designer_id == data.designer_id,
            func.lower(func.trim(PrintModel.name)) == data.name.lower()
        )

        is_designer_have_model = db_session.scalars(stmt).first()

        if is_designer_have_model:
            raise ConflictError("Designer already has a print model with this name")

        print_model = PrintModel(
            name=data.name,
            instructions=data.instructions,
            print_time_minutes=data.print_time_minutes,
            copies=data.copies,
            designer_id=data.designer_id,
            category_id=data.category_id
        )

        db_session.add(print_model)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise ConflictError("Print model violates database constraints")

        db_session.refresh(print_model)
        return print_model

    # Актуализира 3D модел
    def update(self,print_model_id: int,data: PrintModelUpdate,db_session: Session) -> PrintModel:

        print_model = self.get(print_model_id, db_session)

        changes = data.model_dump(exclude_unset=True)

        # Не позволяваме NULL за задължителните полета
        required_fields = (
            "name",
            "instructions",
            "print_time_minutes",
            "copies",
            "designer_id"
        )

        for field in required_fields:
            if field in changes and changes[field] is None:
                raise AppError(f"{field} cannot be null")

        # Проверяваме новия дизайнер, ако се променя
        designer_id = changes.get("designer_id", print_model.designer_id)



        if db_session.get(Designer, designer_id) is None:
            raise NotFound("Designer not found")

        # Проверяваме категорията, ако се променя
        if "category_id" in changes:
            category_id = changes["category_id"]

            if category_id is not None:
                if db_session.get(Category, category_id) is None:
                    raise NotFound("Category not found")

        # Проверяваме уникалността на името за избрания дизайнер
        name = changes.get("name", print_model.name)

        stmt = select(PrintModel).where(
            PrintModel.designer_id == designer_id,
            func.lower(func.trim(PrintModel.name)) == name.lower(),
            PrintModel.id != print_model_id
        )

        is_designer_have_model = db_session.scalars(stmt).first()

        if is_designer_have_model:
            raise ConflictError("Designer already has a print model with this name")

        # Променяме само подадените полета
        for field, value in changes.items():
            setattr(print_model, field, value)

        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            raise ConflictError("Print model update violates database constraints")

        db_session.refresh(print_model)
        return print_model

    # Изтрива 3D модел
    def delete(self, print_model_id: int, db_session: Session) -> int:
        print_model = self.get(print_model_id, db_session)

        db_session.delete(print_model)
        db_session.commit()

        return print_model_id

    # Връща моделите на конкретен дизайнер
    def list_by_designer(self,designer_id: int,db_session: Session) -> list[PrintModel]:

        if db_session.get(Designer, designer_id) is None:
            raise NotFound("Designer not found")

        stmt = select(PrintModel).where(
            PrintModel.designer_id == designer_id
        )

        return list(db_session.scalars(stmt).all())

    # Филтрира 3D моделите по име, категория и максимално време
    def filter(self,db_session: Session,name: str | None = None,category_id: int | None = None,
    max_print_time: int | None = None
    ) -> list[PrintModel]:

        stmt = select(PrintModel)

        if name is not None:
            stmt = stmt.where(
                func.lower(PrintModel.name).contains(name.strip().lower())
            )

        if category_id is not None:
            stmt = stmt.where(PrintModel.category_id == category_id)

        if max_print_time is not None:
            stmt = stmt.where(
                PrintModel.print_time_minutes <= max_print_time
            )

        return list(db_session.scalars(stmt).all())
