import uuid

import pytest
from assertpy import assert_that
from fastapi.testclient import TestClient
from fastapi import FastAPI
from lagom import Container

from python_sprint_zero.domain.repository.coconut_repository import CoconutCommandRepository, CoconutQueryRepository
from python_sprint_zero.infrastructure.persistence.in_memory.in_memory_coconut_command_repository import (
    InMemoryCoconutCommandRepository,
)
from python_sprint_zero.infrastructure.persistence.in_memory.in_memory_coconut_query_repository import (
    InMemoryCoconutQueryRepository,
)
from python_sprint_zero.infrastructure.persistence.in_memory.shared_storage import SharedStorage
from python_sprint_zero.interface.api.controller.coconut_controller import (
    create_coconut_controller,
)


@pytest.fixture(scope="module")
def test_container() -> Container:
    container = Container()

    query_repo = InMemoryCoconutQueryRepository()
    container[CoconutQueryRepository] = lambda: query_repo
    container[CoconutCommandRepository] = InMemoryCoconutCommandRepository

    return container


@pytest.fixture(scope="module")
def test_app(test_container) -> FastAPI:
    app = FastAPI()

    coconut_controller = create_coconut_controller(test_container)
    app.include_router(coconut_controller.router)

    return app


@pytest.fixture
def client(test_app) -> TestClient:
    SharedStorage().clear()
    return TestClient(test_app)


class TestCoconutApi:
    def test_should_create_coconut(self, client):
        coconut_id = uuid.uuid4()

        response = client.post("/coconut/", json={"id": str(coconut_id)})

        assert_that(response.status_code).is_equal_to(201)
        assert_that(response.headers["Location"]).is_equal_to(f"/coconut/{coconut_id}")

    def test_should_retrieve_coconut(self, client):
        coconut_id = uuid.uuid4()

        client.post("/coconut/", json={"id": str(coconut_id)})
        get_response = client.get(f"/coconut/{coconut_id}")

        assert_that(get_response.status_code).is_equal_to(200)

    def test_should_retrieve_coconut_detail(self, client):
        coconut_id = uuid.uuid4()

        client.post("/coconut/", json={"id": str(coconut_id)})
        get_response = client.get(f"/coconut/{coconut_id}")

        assert_that(get_response.json()["id"]).is_equal_to(str(coconut_id))

    def test_should_be_404(self, client):
        nonexistent_id = uuid.uuid4()
        response = client.get(f"/coconut/{nonexistent_id}")

        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()["detail"]).contains("not found")

    def test_should_be_404_detail(self, client):
        nonexistent_id = uuid.uuid4()
        response = client.get(f"/coconut/{nonexistent_id}")

        assert_that(response.json()["detail"]).contains("not found")

    def test_should_be_409(self, client):
        coconut_id = uuid.uuid4()

        client.post("/coconut/", json={"id": str(coconut_id)})
        second_response = client.post("/coconut/", json={"id": str(coconut_id)})

        assert_that(second_response.status_code).is_equal_to(409)

    def test_should_be_409_detail(self, client):
        coconut_id = uuid.uuid4()

        client.post("/coconut/", json={"id": str(coconut_id)})
        second_response = client.post("/coconut/", json={"id": str(coconut_id)})

        assert_that(second_response.json()["detail"]).contains("already exists")
