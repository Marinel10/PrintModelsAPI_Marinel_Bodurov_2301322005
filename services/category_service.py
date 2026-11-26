from __future__ import annotations


from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db.models import Category
from models.category import CategoryCreate, CategoryUpdate
from exceptions import AppError, NotFound, ConflictError


class CategoryService:

    # All categories
    def list(self, db_session: Session) -> list[Category]:

        categories = list(db_session.scalars(select(Category)).all())

        return categories

    # By Id
    def get(self, category_id: int, db_session: Session) -> Category:
        category = db_session.get(Category, category_id)

        if category is None:
            raise NotFound(f"No such category found with id='{category_id}'")

        return category

    def create(self, data: CategoryCreate, db_session: Session) -> Category:
        stmt = select(Category).where(
            func.lower(func.trim(Category.name)) == data.name.lower()
        )

        if db_session.scalars(stmt).first():
            raise ConflictError(f"Category with name '{data.name}' already exists")

        category = Category(name=data.name)

        db_session.add(category)

        try:
            db_session.commit()

        except IntegrityError:
            db_session.rollback()

            raise ConflictError("Category violates database constraints")

        db_session.refresh(category)
        return category


    def update(self,category_id: int,data: CategoryUpdate, db_session: Session) -> Category:

        category = self.get(category_id, db_session)
        changes = data.model_dump(exclude_unset=True)

        if "name" in changes:
            if changes["name"] is None:
                raise AppError("Category name cannot be null")

            stmt = select(Category).where(
                func.lower(func.trim(Category.name)) == changes["name"].lower(),
                Category.id != category_id
            )

            if db_session.scalars(stmt).first():
                raise ConflictError(
                    f"Category with name '{changes['name']}' already exists"
                )

            category.name = changes["name"]

        try:
            db_session.commit()

        except IntegrityError:
            db_session.rollback()

            raise ConflictError("Category update violates database constraints")

        db_session.refresh(category)
        return category


    def delete(self, category_id: int, db_session: Session) -> int:
        category = self.get(category_id, db_session)

        db_session.delete(category)
        db_session.commit()

        return category_id
