import uuid
from typing import List
from unittest.mock import Mock

import pytest

from python_sprint_zero.domain.model.person import Person
from python_sprint_zero.domain.model.relationship import Relationship
from python_sprint_zero.domain.repository.person_repository import PersonQueryRepository, PersonCommandRepository
from python_sprint_zero.domain.repository.relationship_repository import (
    RelationshipQueryRepository,
    RelationshipCommandRepository,
)


@pytest.fixture
def mock_person_query_repository() -> Mock:
    mock_repository = Mock(spec=PersonQueryRepository)
    return mock_repository


@pytest.fixture
def mock_person_command_repository() -> Mock:
    mock_repository = Mock(spec=PersonCommandRepository)
    return mock_repository


@pytest.fixture
def mock_relationship_query_repository() -> Mock:
    mock_repository = Mock(spec=RelationshipQueryRepository)
    return mock_repository


@pytest.fixture
def mock_relationship_command_repository() -> Mock:
    mock_repository = Mock(spec=RelationshipCommandRepository)
    return mock_repository


@pytest.fixture
def sample_person_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def another_person_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def sample_person(sample_person_id) -> Person:
    return Person(id=sample_person_id)


@pytest.fixture
def another_person(another_person_id) -> Person:
    return Person(id=another_person_id)


@pytest.fixture
def sample_relationship(sample_person, another_person) -> Relationship:
    return Relationship(from_person=sample_person, to_person=another_person)


@pytest.fixture
def sample_relationship_list(sample_relationship) -> List[Relationship]:
    return [sample_relationship]
