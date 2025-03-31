from pydantic import UUID4, BaseModel, Field


class Person(BaseModel):
    id: UUID4 = Field(alias="id")
