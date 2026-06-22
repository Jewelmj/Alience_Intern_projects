from fastapi import FastAPI
from schema.utils.startup import (
    initialize_storage
)
initialize_storage()

from api.routes import router

app = FastAPI()

app.include_router(router)