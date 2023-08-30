"""
sama server.
"""
# pylint: disable=wrong-import-position
import logging
import os
import sys

from fastapi import FastAPI
from base.sdk.dfx import DFXClient

sys.path.append(os.path.join('./apps'))

from sama.api import router as sama_router

from base.error import init_error_handler


from celery_app import celery_app


logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(sama_router)
init_error_handler(app)
DFXClient.init()

__all__ = ('celery_app',)
print(app.router.routes)
