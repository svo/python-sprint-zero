import uuid
from typing import Dict

from python_sprint_zero.domain.model.coconut import Coconut
from python_sprint_zero.domain.repository.coconut_repository import CoconutQueryRepository


class InMemoryCoconutQueryRepository(CoconutQueryRepository):
    def __init__(self) -> None:
        self._storage: Dict[uuid.UUID, Coconut] = {}

    def read(self, id: uuid.UUID) -> Coconut:
        print(f"storage: {self._storage}")
        if not isinstance(id, uuid.UUID):
            raise ValueError("Invalid UUID")

        if id not in self._storage:
            raise Exception("Coconut not found")

        return self._storage[id]

    def add_to_storage(self, coconut: Coconut) -> None:
        if coconut.id is None:
            raise ValueError("Coconut ID cannot be None")
        self._storage[coconut.id] = coconut
