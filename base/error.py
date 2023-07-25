"""
Error handler.
"""

import logging

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from base.response import APIResponse


logger = logging.getLogger(__name__)


def init_error_handler(app):
    """
    Initialize the error handler.
    """
    # pylint: disable=unused-argument
    @app.exception_handler(Exception)
    async def error_handler(request, exc):
        """
        Error handler.
        """
        logger.error("【error】 reason: %s", exc)
        return JSONResponse(
            APIResponse(500, "Internal Server Error.")
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request, exc):
        """
        Validation error handler.
        """
        logger.error("【validation error】 reason: %s", exc)
        error = exc.errors()[0]
        return JSONResponse(
            APIResponse(400, f"{error['loc'][-1]}: {error['msg']}")
        )
