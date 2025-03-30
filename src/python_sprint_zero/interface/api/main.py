import sys
import uvicorn
from fastapi import FastAPI

app = FastAPI()


def main(args: list) -> None:
    uvicorn.run(
        "python_sprint_zero.interface.api.main:app",
        reload=True,
    )


def run() -> None:
    main(sys.argv[1:])
