
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.category import CategoryCreate, CategoryRead, CategoryUpdate
from services.category_service import CategoryService


router = APIRouter(prefix="/categories",tags=["Categories"])

category_service = CategoryService()


@router.get("/", response_model=list[CategoryRead])
def list_categories(db_session: Session = Depends(get_db)):
    return category_service.list(db_session)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category( category_id: int, db_session: Session = Depends(get_db)):
    return category_service.get(category_id, db_session)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db_session: Session = Depends(get_db)):
    return category_service.create(data, db_session)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, data: CategoryUpdate,db_session: Session = Depends(get_db)):
    return category_service.update(category_id, data, db_session)


@router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category( category_id: int, db_session: Session = Depends(get_db)):
     category_service.delete(category_id, db_session)
