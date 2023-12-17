from fastapi import FastAPI
from Routers.root_router import root_router


app = FastAPI()

app.include_router(root_router)
