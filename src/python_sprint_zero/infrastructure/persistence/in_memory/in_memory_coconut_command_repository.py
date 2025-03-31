import uuid

from python_sprint_zero.domain.model.coconut import Coconut
from python_sprint_zero.infrastructure.persistence.in_memory.in_memory_coconut_query_repository import (
    InMemoryCoconutQueryRepository,
)


from python_sprint_zero.domain.repository.coconut_repository import CoconutCommandRepository


class InMemoryCoconutCommandRepository(CoconutCommandRepository):
    def __init__(self, query_repository: InMemoryCoconutQueryRepository) -> None:
        self._query_repository = query_repository

    def create(self, coconut: Coconut) -> uuid.UUID:
        if coconut.id is not None:
            try:
                self._query_repository.read(coconut.id)
                raise Exception("Coconut ID already exists")
            except Exception as e:
                if str(e) != "Coconut not found":
                    raise

        id = coconut.id if coconut.id is not None else uuid.uuid4()

        self._query_repository.add_to_storage(Coconut(id=id))

        return id
