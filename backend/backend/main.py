"""Entrypoint of the backend"""

import logging
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.dao.interfaces import DAO
from backend.dao.mysql import Mysql, MysqlConfig
from backend.services.graphql import create_graphql_app


def init_dao() -> DAO:
    """Initialize a database access object."""
    config = MysqlConfig(host="mysql", password=os.environ["DATABASE_PASSWORD"])
    dao_instance = Mysql(config=config)
    return dao_instance


def start_server():
    """Launched with `poetry run startServer` at root level"""
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)


# TODO: Use env variable for level
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

app = FastAPI()
dao = init_dao()
graphql_app = create_graphql_app(dao=dao)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/query")
