import uvicorn
import logging
import os
from fastapi import FastAPI
from backend.dao.interfaces import DAO
from backend.dao.mysql import Mysql, MysqlConfig
from backend.services.graphql import createGraphqlApp


def initDao() -> DAO:
    config = MysqlConfig(host="mysql", password=os.environ["DATABASE_PASSWORD"])
    dao = Mysql(config=config)
    return dao


def startServer():
    """Launched with `poetry run startServer` at root level"""
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)


# TODO: Use env variable for level
logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

app = FastAPI()
dao = initDao()
graphql_app = createGraphqlApp(dao=dao)

app.include_router(graphql_app, prefix="/query")
