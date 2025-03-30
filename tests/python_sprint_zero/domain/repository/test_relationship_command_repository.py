import uuid

import pytest
from assertpy import assert_that
from unittest.mock import Mock


class TestRelationshipCommandRepository:
    def test_should_create_relationship_successfully(
        self, mock_relationship_command_repository: Mock, sample_person_id: uuid.UUID, another_person_id: uuid.UUID
    ):
        mock_relationship_command_repository.create.return_value = None

        result = mock_relationship_command_repository.create(sample_person_id, another_person_id)

        assert_that(result).is_none()
        mock_relationship_command_repository.create.assert_called_once_with(sample_person_id, another_person_id)

    def test_should_throw_exception_when_create_fails(
        self, mock_relationship_command_repository: Mock, sample_person_id: uuid.UUID, another_person_id: uuid.UUID
    ):
        mock_relationship_command_repository.create.side_effect = Exception("Relationship creation failed")

        with pytest.raises(Exception) as excinfo:
            mock_relationship_command_repository.create(sample_person_id, another_person_id)

        assert_that(str(excinfo.value)).is_equal_to("Relationship creation failed")
        mock_relationship_command_repository.create.assert_called_once_with(sample_person_id, another_person_id)

    def test_should_throw_exception_when_relationship_already_exists(
        self, mock_relationship_command_repository: Mock, sample_person_id: uuid.UUID, another_person_id: uuid.UUID
    ):
        mock_relationship_command_repository.create.side_effect = Exception("Relationship already exists")

        with pytest.raises(Exception) as excinfo:
            mock_relationship_command_repository.create(sample_person_id, another_person_id)

        assert_that(str(excinfo.value)).is_equal_to("Relationship already exists")
        mock_relationship_command_repository.create.assert_called_once_with(sample_person_id, another_person_id)

    def test_should_throw_exception_when_from_person_id_is_invalid(
        self, mock_relationship_command_repository: Mock, another_person_id: uuid.UUID
    ):
        invalid_id = "not-a-uuid"
        mock_relationship_command_repository.create.side_effect = ValueError("Invalid from_person UUID")

        with pytest.raises(ValueError) as excinfo:
            mock_relationship_command_repository.create(invalid_id, another_person_id)

        assert_that(str(excinfo.value)).is_equal_to("Invalid from_person UUID")
        mock_relationship_command_repository.create.assert_called_once_with(invalid_id, another_person_id)

    def test_should_throw_exception_when_to_person_id_is_invalid(
        self, mock_relationship_command_repository: Mock, sample_person_id: uuid.UUID
    ):
        invalid_id = "not-a-uuid"
        mock_relationship_command_repository.create.side_effect = ValueError("Invalid to_person UUID")

        with pytest.raises(ValueError) as excinfo:
            mock_relationship_command_repository.create(sample_person_id, invalid_id)

        assert_that(str(excinfo.value)).is_equal_to("Invalid to_person UUID")
        mock_relationship_command_repository.create.assert_called_once_with(sample_person_id, invalid_id)
