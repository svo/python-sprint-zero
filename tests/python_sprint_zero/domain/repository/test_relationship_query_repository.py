import uuid
from typing import List

import pytest
from assertpy import assert_that
from unittest.mock import Mock

from python_sprint_zero.domain.model.relationship import Relationship


class TestRelationshipQueryRepository:
    def test_should_return_relationship_list_when_exists(
        self,
        mock_relationship_query_repository: Mock,
        sample_person_id: uuid.UUID,
        another_person_id: uuid.UUID,
        sample_relationship_list: List[Relationship],
    ):
        mock_relationship_query_repository.read.return_value = sample_relationship_list

        result = mock_relationship_query_repository.read(sample_person_id, another_person_id)

        assert_that(result).is_equal_to(sample_relationship_list)
        mock_relationship_query_repository.read.assert_called_once_with(sample_person_id, another_person_id)

    def test_should_return_relationship_with_correct_from_person_id(
        self,
        mock_relationship_query_repository: Mock,
        sample_person_id: uuid.UUID,
        another_person_id: uuid.UUID,
        sample_relationship_list: List[Relationship],
    ):
        mock_relationship_query_repository.read.return_value = sample_relationship_list

        result = mock_relationship_query_repository.read(sample_person_id, another_person_id)

        assert_that(result[0].from_person.id).is_equal_to(sample_person_id)
        mock_relationship_query_repository.read.assert_called_once_with(sample_person_id, another_person_id)

    def test_should_return_relationship_with_correct_to_person_id(
        self,
        mock_relationship_query_repository: Mock,
        sample_person_id: uuid.UUID,
        another_person_id: uuid.UUID,
        sample_relationship_list: List[Relationship],
    ):
        mock_relationship_query_repository.read.return_value = sample_relationship_list

        result = mock_relationship_query_repository.read(sample_person_id, another_person_id)

        assert_that(result[0].to_person.id).is_equal_to(another_person_id)
        mock_relationship_query_repository.read.assert_called_once_with(sample_person_id, another_person_id)

    def test_should_return_empty_list_when_no_relationship_exists(
        self, mock_relationship_query_repository: Mock, sample_person_id: uuid.UUID, another_person_id: uuid.UUID
    ):
        mock_relationship_query_repository.read.return_value = []

        result = mock_relationship_query_repository.read(sample_person_id, another_person_id)

        assert_that(result).is_empty()
        mock_relationship_query_repository.read.assert_called_once_with(sample_person_id, another_person_id)

    def test_should_throw_exception_when_from_person_id_is_invalid(
        self, mock_relationship_query_repository: Mock, another_person_id: uuid.UUID
    ):
        invalid_id = "not-a-uuid"
        mock_relationship_query_repository.read.side_effect = ValueError("Invalid from_person UUID")

        with pytest.raises(ValueError) as excinfo:
            mock_relationship_query_repository.read(invalid_id, another_person_id)

        assert_that(str(excinfo.value)).is_equal_to("Invalid from_person UUID")
        mock_relationship_query_repository.read.assert_called_once_with(invalid_id, another_person_id)

    def test_should_throw_exception_when_to_person_id_is_invalid(
        self, mock_relationship_query_repository: Mock, sample_person_id: uuid.UUID
    ):
        invalid_id = "not-a-uuid"
        mock_relationship_query_repository.read.side_effect = ValueError("Invalid to_person UUID")

        with pytest.raises(ValueError) as excinfo:
            mock_relationship_query_repository.read(sample_person_id, invalid_id)

        assert_that(str(excinfo.value)).is_equal_to("Invalid to_person UUID")
        mock_relationship_query_repository.read.assert_called_once_with(sample_person_id, invalid_id)

    def test_should_throw_exception_when_repository_fails(
        self, mock_relationship_query_repository: Mock, sample_person_id: uuid.UUID, another_person_id: uuid.UUID
    ):
        mock_relationship_query_repository.read.side_effect = Exception("Repository failure")

        with pytest.raises(Exception) as excinfo:
            mock_relationship_query_repository.read(sample_person_id, another_person_id)

        assert_that(str(excinfo.value)).is_equal_to("Repository failure")
        mock_relationship_query_repository.read.assert_called_once_with(sample_person_id, another_person_id)
