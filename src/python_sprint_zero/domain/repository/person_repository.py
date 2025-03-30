import uuid

from abc import ABC, abstractmethod

from python_sprint_zero.domain.model.person import Person


class PersonQueryRepository(ABC):
    @abstractmethod
    def read(self, id: uuid.UUID) -> Person:
        raise NotImplementedError()


class PersonCommandRepository(ABC):
    @abstractmethod
    def create(self, id: uuid.UUID) -> str:
        raise NotImplementedError()
