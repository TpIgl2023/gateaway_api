from fastapi import FastAPI

from Routers.adminRestrictedPage import adminRouter
from Routers.loginRouter import loginRouter
from Routers.rootRouter import rootRouter


app = FastAPI()

app.include_router(loginRouter, prefix="/login")
app.include_router(rootRouter)
app.include_router(adminRouter, prefix="/admin")


# You can start the server by running : uvicorn main:app --reload

