from pydantic import BaseModel, Field

from python_sprint_zero.domain.model.person import Person


class Relationship(BaseModel):
    from_person: Person = Field(alias="from_person")
    to_person: Person = Field(alias="to_person")
