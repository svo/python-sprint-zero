from unittest.mock import Mock

import pytest
from assertpy import assert_that
from fastapi import FastAPI
from fastapi.testclient import TestClient

from python_sprint_zero.application.use_case.coconut_use_case import CreateCoconutUseCase, GetCoconutUseCase
from python_sprint_zero.domain.model.coconut import Coconut
from python_sprint_zero.interface.api.controller.coconut_controller import CoconutController


class TestCoconutController:
    @pytest.fixture
    def mock_get_coconut_use_case(self) -> Mock:
        mock = Mock(spec=GetCoconutUseCase)
        return mock

    @pytest.fixture
    def mock_create_coconut_use_case(self) -> Mock:
        mock = Mock(spec=CreateCoconutUseCase)
        return mock

    @pytest.fixture
    def controller(self, mock_get_coconut_use_case, mock_create_coconut_use_case) -> CoconutController:
        return CoconutController(
            get_coconut_use_case=mock_get_coconut_use_case,
            create_coconut_use_case=mock_create_coconut_use_case,
        )

    @pytest.fixture
    def app(self, controller) -> FastAPI:
        app = FastAPI()
        app.include_router(controller.router)
        return app

    @pytest.fixture
    def client(self, app) -> TestClient:
        return TestClient(app)

    def test_should_be_200(self, client, mock_get_coconut_use_case, sample_coconut_id):
        coconut = Coconut(id=sample_coconut_id)
        mock_get_coconut_use_case.execute.return_value = coconut

        response = client.get(f"/coconut/{sample_coconut_id}")

        assert_that(response.status_code).is_equal_to(200)
        mock_get_coconut_use_case.execute.assert_called_once_with(sample_coconut_id)

    def test_should_get_coconut(self, client, mock_get_coconut_use_case, sample_coconut_id):
        coconut = Coconut(id=sample_coconut_id)
        mock_get_coconut_use_case.execute.return_value = coconut

        response = client.get(f"/coconut/{sample_coconut_id}")

        assert_that(response.json()["id"]).is_equal_to(str(sample_coconut_id))

    def test_should_be_404(self, client, mock_get_coconut_use_case, sample_coconut_id):
        mock_get_coconut_use_case.execute.side_effect = Exception("Coconut not found")

        response = client.get(f"/coconut/{sample_coconut_id}")

        assert_that(response.status_code).is_equal_to(404)
        mock_get_coconut_use_case.execute.assert_called_once_with(sample_coconut_id)

    def test_should_have_message_detail_when_404(self, client, mock_get_coconut_use_case, sample_coconut_id):
        mock_get_coconut_use_case.execute.side_effect = Exception("Coconut not found")

        response = client.get(f"/coconut/{sample_coconut_id}")

        assert_that(response.json()["detail"]).contains("not found")

    def test_should_be_201(self, client, mock_create_coconut_use_case, sample_coconut_id):
        mock_create_coconut_use_case.execute.return_value = sample_coconut_id
        request_data = {"id": str(sample_coconut_id)}

        response = client.post("/coconut/", json=request_data)

        assert_that(response.status_code).is_equal_to(201)
        mock_create_coconut_use_case.execute.assert_called_once()

    def test_should_have_new_id_in_location_header(self, client, mock_create_coconut_use_case, sample_coconut_id):
        mock_create_coconut_use_case.execute.return_value = sample_coconut_id
        request_data = {"id": str(sample_coconut_id)}

        response = client.post("/coconut/", json=request_data)

        assert_that(response.headers["Location"]).is_equal_to(f"/coconut/{sample_coconut_id}")

    def test_should_use_create_use_case(self, client, mock_create_coconut_use_case, sample_coconut_id):
        mock_create_coconut_use_case.execute.return_value = sample_coconut_id
        request_data = {"id": str(sample_coconut_id)}

        client.post("/coconut/", json=request_data)

        mock_create_coconut_use_case.execute.assert_called_once()

    def test_should_pass_id_to_create_use_case(self, client, mock_create_coconut_use_case, sample_coconut_id):
        mock_create_coconut_use_case.execute.return_value = sample_coconut_id
        request_data = {"id": str(sample_coconut_id)}

        client.post("/coconut/", json=request_data)

        mock_create_coconut_use_case.execute.assert_called_once_with(sample_coconut_id)

    def test_should_be_409(self, client, mock_create_coconut_use_case, sample_coconut_id):
        mock_create_coconut_use_case.execute.side_effect = Exception("Coconut ID already exists")
        request_data = {"id": str(sample_coconut_id)}

        response = client.post("/coconut/", json=request_data)

        assert_that(response.status_code).is_equal_to(409)
        mock_create_coconut_use_case.execute.assert_called_once()

    def test_should_raise_error_when_already_exists(self, client, mock_create_coconut_use_case, sample_coconut_id):
        mock_create_coconut_use_case.execute.side_effect = Exception("Coconut ID already exists")
        request_data = {"id": str(sample_coconut_id)}

        response = client.post("/coconut/", json=request_data)

        assert_that(response.json()["detail"]).contains("already exists")

    def test_should_be_500(self, client, mock_get_coconut_use_case, sample_coconut_id):
        mock_get_coconut_use_case.execute.side_effect = Exception("Database connection error")

        response = client.get(f"/coconut/{sample_coconut_id}")

        assert_that(response.status_code).is_equal_to(500)
        mock_get_coconut_use_case.execute.assert_called_once_with(sample_coconut_id)

    def test_should_have_message_detail_when_500(self, client, mock_get_coconut_use_case, sample_coconut_id):
        mock_get_coconut_use_case.execute.side_effect = Exception("Database connection error")

        response = client.get(f"/coconut/{sample_coconut_id}")

        assert_that(response.json()["detail"]).contains("Error retrieving coconut")

    def test_should_be_400(self, client, mock_create_coconut_use_case, sample_coconut_id):
        mock_create_coconut_use_case.execute.side_effect = Exception("Validation error")
        request_data = {"id": str(sample_coconut_id)}

        response = client.post("/coconut/", json=request_data)

        assert_that(response.status_code).is_equal_to(400)
        mock_create_coconut_use_case.execute.assert_called_once()

    def test_should_have_message_detail_when_400(self, client, mock_create_coconut_use_case, sample_coconut_id):
        mock_create_coconut_use_case.execute.side_effect = Exception("Validation error")
        request_data = {"id": str(sample_coconut_id)}

        response = client.post("/coconut/", json=request_data)

        assert_that(response.json()["detail"]).contains("Error creating coconut")
