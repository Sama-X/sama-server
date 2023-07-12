"""
sama server.
"""
import os
import sys

from fastapi import FastAPI

sys.path.append(os.path.join('./apps'))

from sama.api import router as sama_router


app = FastAPI()
app.include_router(sama_router)

print(app.router.routes)
