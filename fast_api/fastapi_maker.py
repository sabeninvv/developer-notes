import os
from typing import Dict, Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import uvicorn
from fastapi import Request, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse, JSONResponse, HTMLResponse


def make_fastAPI_app() -> FastAPI:
    module_version = os.getenv("MODULE_VERSION", "no_version")
    app = FastAPI(title="Title module",
                  description="Server creates video Potpourri and Trailer",
                  version=module_version,
                  docs_url=None)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET, POST, OPTIONS"],
        allow_headers=["DNT, User-Agent, X-Requested-With, If-Modified-Since, Cache-Control, Content-Type, Range"],
        expose_headers=["Content-Length, Content-Range"],
        max_age=600
    )
    return app


async def common_query_params(q_param_1: int = 10, q_param_2: float = .5) -> Dict[str, Union[int, float]]:
    return {
        "q_param_1": q_param_1,
        "q_param_2": q_param_2
    }
