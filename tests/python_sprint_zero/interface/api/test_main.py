import json
import os

from fastapi.openapi.utils import get_openapi
from assertpy import assert_that
from unittest.mock import patch

from python_sprint_zero.interface.api.main import run

OPENAPI_JSON_FILE_PATH = "build/openapi.json"
OPENAPI_JSON_FILE_PATH_OPEN_FLAG = "w"


def create_openapi_json(app):
    os.makedirs(os.path.dirname(OPENAPI_JSON_FILE_PATH), exist_ok=True)

    with open(OPENAPI_JSON_FILE_PATH, OPENAPI_JSON_FILE_PATH_OPEN_FLAG) as json_output_file:
        json.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
            ),
            json_output_file,
        )


def test_should_create_openapi_json_file():
    if os.path.exists(OPENAPI_JSON_FILE_PATH):
        os.remove(OPENAPI_JSON_FILE_PATH)

    from python_sprint_zero.interface.api.main import app as rest

    create_openapi_json(rest)

    assert_that(OPENAPI_JSON_FILE_PATH).exists()


@patch("python_sprint_zero.interface.api.main.main")
@patch("sys.argv", ["test_script.py", "some_arg"])
def test_should_run_main_function_with_command_line_args(mock_main):
    run()

    mock_main.assert_called_once_with(["some_arg"])


@patch("uvicorn.run")
def test_should_start_uvicorn_server_with_correct_parameters(mock_uvicorn_run):
    from python_sprint_zero.interface.api.main import main

    main([])

    mock_uvicorn_run.assert_called_once_with(
        "python_sprint_zero.interface.api.main:app",
        reload=True,
    )
