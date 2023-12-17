from fastapi import FastAPI

from Routers.loginRouter import loginRouter
from Routers.root_router import root_router


app = FastAPI()

app.include_router(loginRouter, prefix="/login")
app.include_router(root_router)




# You can start the server by running : uvicorn main:app --reload

