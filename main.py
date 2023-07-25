"""
sama server.
"""
# pylint: disable=wrong-import-position
import logging
import os
import sys

from fastapi import FastAPI

sys.path.append(os.path.join('./apps'))

from sama.api import router as sama_router

from base.error import init_error_handler


logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(sama_router)
init_error_handler(app)

print(app.router.routes)
