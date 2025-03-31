import uuid
from unittest.mock import Mock

import pytest

from python_sprint_zero.domain.model.coconut import Person
from python_sprint_zero.domain.repository.coconut_repository import PersonQueryRepository, PersonCommandRepository


@pytest.fixture
def mock_coconut_query_repository() -> Mock:
    mock_repository = Mock(spec=PersonQueryRepository)
    return mock_repository


@pytest.fixture
def mock_coconut_command_repository() -> Mock:
    mock_repository = Mock(spec=PersonCommandRepository)
    return mock_repository


@pytest.fixture
def sample_coconut_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def another_coconut_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def sample_coconut(sample_coconut_id) -> Person:
    return Person(id=sample_coconut_id)


@pytest.fixture
def another_coconut(another_coconut_id) -> Person:
    return Person(id=another_coconut_id)
