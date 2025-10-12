import logging
from logging import Logger
from typing import Dict

from fastapi import Request
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from common import CommonConstants, FileToProcessError


class ExceptionMiddleware(BaseHTTPMiddleware):
    logger: Logger = logging.getLogger(CommonConstants.SERVICE_NAME)

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.exception_handlers: Dict = {
            TimeoutError: self.handle_timeout_error,
            ValueError: self.handle_value_error,
            FileToProcessError: self.handle_file_error,
        }

    async def handle_timeout_error(self, request: Request, exc: TimeoutError):
        self.logger.error(f"TimeoutError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"detail": "There were problems sending the request"}
        )

    async def handle_value_error(self, request: Request, exc: ValueError):
        self.logger.error(f"ValueError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Incorrect value"}
        )

    async def handle_file_error(self, request: Request, exc: FileToProcessError):
        self.logger.error(f"FileToProcessError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message}
        )

    async def handle_generic_exception(self, request: Request, exc: Exception):
        self.logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            handler = self.exception_handlers.get(type(exc))
            if handler:
                return await handler(request, exc)
            else:
                return await self.handle_generic_exception(request, exc)
