
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Designer
from models.designer import DesignerCreate, DesignerRead, DesignerUpdate
from services.designer_service import DesignerService


router = APIRouter(prefix="/designers",tags=["Designers"])

designers_service = DesignerService()


# All designers
@router.get("/", response_model=list[DesignerRead])
def list_designers(db_session: Session = Depends(get_db)):
    return designers_service.list(db_session)


# Designer by ID
@router.get("/{designer_id}", response_model=DesignerRead)
def get_designer(designer_id: int, db_session: Session = Depends(get_db)):
    return designers_service.get(designer_id, db_session)


# Create Designer
@router.post("/",response_model=DesignerRead,status_code=status.HTTP_201_CREATED)
def create_designer(data: DesignerCreate, db_session: Session = Depends(get_db)):
    return designers_service.create(data, db_session)


# Uppdate Designer by ID
@router.put("/{designer_id}", response_model=DesignerRead)
def update_designer(designer_id: int, data: DesignerUpdate, db_session: Session = Depends(get_db)):
    return designers_service.update(designer_id, data, db_session)


# Delete Designer by ID
@router.delete("/{designer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_designer(designer_id: int, db_session: Session = Depends(get_db)):
    designers_service.delete(designer_id, db_session)
