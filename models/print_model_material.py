from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class MaterialUnit(str, Enum):
    g = "g"
    m = "m"
    ml = "ml"


class PrintModelMaterialCreate(BaseModel):
    material_id: int = Field(gt=0)
    quantity: float = Field(gt=0)
    unit: MaterialUnit


class PrintModelMaterialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    print_model_id: int
    material_id: int
    quantity: float
    unit: MaterialUnit


class PrintModelMaterialUpdate(BaseModel):
    quantity: float | None = Field(default=None, gt=0)
    unit: MaterialUnit | None = None