import uuid

from abc import ABC, abstractmethod
from typing import List

from python_sprint_zero.domain.model.relationship import Relationship


class RelationshipQueryRepository(ABC):
    @abstractmethod
    def read(self, from_person: uuid.UUID, to_person: uuid.UUID) -> List[Relationship]:
        raise NotImplementedError()


class RelationshipCommandRepository(ABC):
    @abstractmethod
    def create(self, from_person: uuid.UUID, to_person: uuid.UUID) -> None:
        raise NotImplementedError()
