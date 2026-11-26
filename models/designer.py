from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class DesignerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=110)
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Designer name cannot be empty")

        return value


class DesignerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class DesignerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1,max_length=110)
    email: EmailStr | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Designer name cannot be empty")

        return value