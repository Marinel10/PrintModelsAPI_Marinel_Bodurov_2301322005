
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.material import MaterialCreate, MaterialRead, MaterialUpdate
from services.material_service import MaterialService


router = APIRouter( prefix="/materials", tags=["Materials"] )

material_service = MaterialService()


@router.get("/", response_model=list[MaterialRead])
def list_materials(db_session: Session = Depends(get_db)):
    return material_service.list(db_session)


@router.get("/{material_id}", response_model=MaterialRead)
def get_material( material_id: int,  db_session: Session = Depends(get_db)):
    return material_service.get(material_id, db_session)


@router.post( "/", response_model=MaterialRead, status_code=status.HTTP_201_CREATED)
def create_material( data: MaterialCreate, db_session: Session = Depends(get_db)):
    return material_service.create(data, db_session)


@router.put("/{material_id}", response_model=MaterialRead)
def update_material( material_id: int, data: MaterialUpdate, db_session: Session = Depends(get_db)):
    return material_service.update(material_id, data, db_session)


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material( material_id: int, db_session: Session = Depends(get_db)):
    material_service.delete(material_id, db_session)
