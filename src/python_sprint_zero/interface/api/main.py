import sys
import uvicorn
from fastapi import FastAPI
from lagom import Container

from python_sprint_zero.application.use_case.coconut_use_case import CreateCoconutUseCase, GetCoconutUseCase
from python_sprint_zero.domain.repository.coconut_repository import CoconutCommandRepository, CoconutQueryRepository
from python_sprint_zero.infrastructure.persistence.in_memory.in_memory_coconut_command_repository import (
    InMemoryCoconutCommandRepository,
)
from python_sprint_zero.infrastructure.persistence.in_memory.in_memory_coconut_query_repository import (
    InMemoryCoconutQueryRepository,
)
from python_sprint_zero.interface.api.controller.coconut_controller import (
    create_coconut_controller,
)

app = FastAPI(title="Python Sprint Zero API", version="1.0.0")


def get_container() -> Container:
    container = Container()

    query_repo = InMemoryCoconutQueryRepository()
    command_repo = InMemoryCoconutCommandRepository(query_repo)

    container[CoconutQueryRepository] = lambda: query_repo  # type: ignore
    container[CoconutCommandRepository] = lambda: command_repo  # type: ignore

    container[GetCoconutUseCase] = GetCoconutUseCase
    container[CreateCoconutUseCase] = CreateCoconutUseCase

    return container


global_container = get_container()


def get_global_container() -> Container:
    return global_container


coconut_controller = create_coconut_controller(global_container)
app.include_router(coconut_controller.router)


def main(args: list) -> None:
    uvicorn.run(
        "python_sprint_zero.interface.api.main:app",
        reload=True,
    )


def run() -> None:
    main(sys.argv[1:])
