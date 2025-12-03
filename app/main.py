import logging
import subprocess

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from logging.config import dictConfig

from common import LOGGING_CONFIG, DbConstants, CommonConstants
from routers import voice_router, llm_router, image_router
from middleware import ExceptionMiddleware
from routers import history_router


def run_migrations():
    process = subprocess.run(
        [
            "pyway", "migrate",
            "--database-migration-dir", DbConstants.PYWAY_DATABASE_MIGRATION_DIR,
            "--database-table", DbConstants.PYWAY_TABLE,
            "--database-type", DbConstants.PYWAY_TYPE,
            "--database-host", DbConstants.DB_HOST,
            "--database-port", DbConstants.DB_PORT,
            "--database-name", DbConstants.DB_NAME,
            "--database-username", DbConstants.DB_USER,
            "--database-password", DbConstants.DB_PASSWORD
        ]
    )
    logging.debug(process.stdout)
    if process.returncode != 0:
        logging.error(process.stderr)
        raise ValueError("Cannot migrate database")


app = FastAPI()

# noinspection PyTypeChecker
app.add_middleware(ExceptionMiddleware)
# noinspection PyTypeChecker
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"] )
app.include_router(voice_router)
app.include_router(llm_router)
app.include_router(history_router)
app.include_router(image_router)
dictConfig(LOGGING_CONFIG)

if DbConstants.PYWAY_ENABLED:
    run_migrations()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=LOGGING_CONFIG)
