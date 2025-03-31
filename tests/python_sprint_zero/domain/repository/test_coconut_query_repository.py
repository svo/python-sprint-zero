import uuid

import pytest
from assertpy import assert_that
from unittest.mock import Mock

from python_sprint_zero.domain.model.coconut import Person


class TestPersonQueryRepository:
    def test_should_return_coconut_when_exists(
        self, mock_coconut_query_repository: Mock, sample_coconut_id: uuid.UUID, sample_coconut: Person
    ):
        mock_coconut_query_repository.read.return_value = sample_coconut

        result = mock_coconut_query_repository.read(sample_coconut_id)

        assert_that(result).is_equal_to(sample_coconut)
        mock_coconut_query_repository.read.assert_called_once_with(sample_coconut_id)

    def test_should_return_coconut_with_correct_id(
        self, mock_coconut_query_repository: Mock, sample_coconut_id: uuid.UUID, sample_coconut: Person
    ):
        mock_coconut_query_repository.read.return_value = sample_coconut

        result = mock_coconut_query_repository.read(sample_coconut_id)

        assert_that(result.id).is_equal_to(sample_coconut_id)
        mock_coconut_query_repository.read.assert_called_once_with(sample_coconut_id)

    def test_should_throw_exception_when_coconut_does_not_exist(
        self, mock_coconut_query_repository: Mock, sample_coconut_id: uuid.UUID
    ):
        mock_coconut_query_repository.read.side_effect = Exception("Person not found")

        with pytest.raises(Exception) as excinfo:
            mock_coconut_query_repository.read(sample_coconut_id)

        assert_that(str(excinfo.value)).is_equal_to("Person not found")
        mock_coconut_query_repository.read.assert_called_once_with(sample_coconut_id)

    def test_should_throw_exception_when_id_is_invalid(self, mock_coconut_query_repository: Mock):
        invalid_id = "not-a-uuid"
        mock_coconut_query_repository.read.side_effect = ValueError("Invalid UUID")

        with pytest.raises(ValueError) as excinfo:
            mock_coconut_query_repository.read(invalid_id)

        assert_that(str(excinfo.value)).is_equal_to("Invalid UUID")
        mock_coconut_query_repository.read.assert_called_once_with(invalid_id)

    def test_should_throw_exception_when_repository_fails(
        self, mock_coconut_query_repository: Mock, sample_coconut_id: uuid.UUID
    ):
        mock_coconut_query_repository.read.side_effect = Exception("Repository failure")

        with pytest.raises(Exception) as excinfo:
            mock_coconut_query_repository.read(sample_coconut_id)

        assert_that(str(excinfo.value)).is_equal_to("Repository failure")
        mock_coconut_query_repository.read.assert_called_once_with(sample_coconut_id)
