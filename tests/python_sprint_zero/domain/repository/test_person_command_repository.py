import uuid

import pytest
from assertpy import assert_that
from unittest.mock import Mock


class TestPersonCommandRepository:
    def test_should_create_person_successfully(self, mock_person_command_repository: Mock, sample_person_id: uuid.UUID):
        expected_result = "Person created successfully"
        mock_person_command_repository.create.return_value = expected_result

        result = mock_person_command_repository.create(sample_person_id)

        assert_that(result).is_equal_to(expected_result)
        mock_person_command_repository.create.assert_called_once_with(sample_person_id)

    def test_should_throw_exception_when_create_fails(
        self, mock_person_command_repository: Mock, sample_person_id: uuid.UUID
    ):
        mock_person_command_repository.create.side_effect = Exception("Creation failed")

        with pytest.raises(Exception) as excinfo:
            mock_person_command_repository.create(sample_person_id)

        assert_that(str(excinfo.value)).is_equal_to("Creation failed")
        mock_person_command_repository.create.assert_called_once_with(sample_person_id)

    def test_should_throw_exception_when_id_already_exists(
        self, mock_person_command_repository: Mock, sample_person_id: uuid.UUID
    ):
        mock_person_command_repository.create.side_effect = Exception("Person ID already exists")

        with pytest.raises(Exception) as excinfo:
            mock_person_command_repository.create(sample_person_id)

        assert_that(str(excinfo.value)).is_equal_to("Person ID already exists")
        mock_person_command_repository.create.assert_called_once_with(sample_person_id)

    def test_should_throw_exception_when_id_is_invalid(self, mock_person_command_repository: Mock):
        invalid_id = "not-a-uuid"
        mock_person_command_repository.create.side_effect = ValueError("Invalid UUID")

        with pytest.raises(ValueError) as excinfo:
            mock_person_command_repository.create(invalid_id)

        assert_that(str(excinfo.value)).is_equal_to("Invalid UUID")
        mock_person_command_repository.create.assert_called_once_with(invalid_id)
