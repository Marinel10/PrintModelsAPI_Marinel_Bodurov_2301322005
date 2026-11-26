from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.print_model_material import (
    PrintModelMaterialCreate,
    PrintModelMaterialRead,
    PrintModelMaterialUpdate
)
from services.print_model_material_service import PrintModelMaterialService


router = APIRouter(prefix="/print-models",tags=["Print Model Materials"])

material_service = PrintModelMaterialService()


# All material for Model
@router.get( "/{print_model_id}/materials", response_model=list[PrintModelMaterialRead])
def list_model_materials( print_model_id: int, db_session: Session = Depends(get_db)):
    return material_service.list(print_model_id, db_session)


# Add material to Model
@router.post("/{print_model_id}/materials", response_model=PrintModelMaterialRead, status_code=status.HTTP_201_CREATED)
def add_model_material(print_model_id: int, data: PrintModelMaterialCreate, db_session: Session = Depends(get_db)):
    return material_service.create(print_model_id, data, db_session)


# Edit material unit / quantity
@router.put("/{print_model_id}/materials/{material_id}", response_model=PrintModelMaterialRead)
def update_model_material( print_model_id: int, material_id: int, data: PrintModelMaterialUpdate, db_session: Session = Depends(get_db)):
    return material_service.update(print_model_id, material_id, data , db_session )


# Remove material from Model
@router.delete("/{print_model_id}/materials/{material_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_model_material(print_model_id: int, material_id: int, db_session: Session = Depends(get_db)):
    material_service.delete(print_model_id, material_id, db_session)


# Recalculate Model copies materials
@router.get("/{print_model_id}/recalculate")
def recalculate_materials( print_model_id: int, copies: int = Query(ge=1, le=55), db_session: Session = Depends(get_db) ):
    return material_service.recalculate( print_model_id, copies,  db_session )
