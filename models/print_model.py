from pydantic import BaseModel, Field, ConfigDict, field_validator


class PrintModelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    instructions: str = Field(min_length=1, max_length=1000)
    print_time_minutes: int = Field(gt=0)
    copies: int = Field(gt=0)
    designer_id: int = Field(gt=0)
    category_id: int | None = Field(default=None, gt=0)
    difficulty:str | None = Field(default="medium", gt=0)

    @field_validator("name", "instructions")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value


class PrintModelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    instructions: str
    print_time_minutes: int
    copies: int
    designer_id: int
    category_id: int | None
    difficulty: str


class PrintModelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    instructions: str | None = Field(default=None, min_length=1, max_length=1000)
    print_time_minutes: int | None = Field(default=None, gt=0)
    copies: int | None = Field(default=None, gt=0)
    designer_id: int | None = Field(default=None, gt=0)
    category_id: int | None = Field(default=None, gt=0)
    difficulty: str | None = Field(default="medium", gt=0)

    @field_validator("name", "instructions")
    @classmethod
    def validate_text(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value