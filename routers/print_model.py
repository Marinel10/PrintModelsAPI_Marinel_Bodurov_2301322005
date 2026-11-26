
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.print_model import (
    PrintModelCreate,
    PrintModelRead,
    PrintModelUpdate
)
from services.print_model_service import PrintModelService


router = APIRouter(prefix="/print-models", tags=["Print Models"])

designer_models_router = APIRouter( prefix="/designers", tags=["Designers"])

model_service = PrintModelService()


# All 3D models
@router.get("/", response_model=list[PrintModelRead])
def list_models( name: str | None = None,
    category_id: int | None = Query(default=None, gt=0),
    max_print_time: int | None = Query(default=None, gt=0),
    db_session: Session = Depends(get_db)
):
    return model_service.filter( db_session,
                                 name=name,
                                 category_id=category_id,
                                 max_print_time=max_print_time
                                 )


# All 3D models by Desinger
@designer_models_router.get("/{designer_id}/print-models", response_model=list[PrintModelRead])

def list_by_designer( designer_id: int,db_session: Session = Depends(get_db)):
    return model_service.list_by_designer(designer_id, db_session)


# Model by ID
@router.get("/{print_model_id}", response_model=PrintModelRead)

def get_model(print_model_id: int,db_session: Session = Depends(get_db)):
    return model_service.get(print_model_id, db_session)


# Create 3D Model
@router.post( "/",response_model=PrintModelRead,status_code=status.HTTP_201_CREATED)

def create_model( data: PrintModelCreate,db_session: Session = Depends(get_db)):
    return model_service.create(data, db_session)


# Patch Model
@router.put("/{print_model_id}", response_model=PrintModelRead)

def update_model(print_model_id: int, data: PrintModelUpdate, db_session: Session = Depends(get_db)):
    return model_service.update(print_model_id, data, db_session)


# Delete Model
@router.delete("/{print_model_id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_model(print_model_id: int, db_session: Session = Depends(get_db)):
    model_service.delete(print_model_id, db_session)
