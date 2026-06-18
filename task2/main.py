from fastapi import FastAPI
from api.routes import router
from schema.utils.startup import (
    initialize_storage
)

app = FastAPI()

initialize_storage()

app.include_router(router)