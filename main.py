import uvicorn
from fastapi import FastAPI

from Routers.adminRouter import adminRouter
from Routers.authRouter import authRouter
from Routers.rootRouter import rootRouter
from Routers.root_router import root_router
from Routers.articlesRouter import articlesRouter
from Routers.profileRouter import profileRouter


app = FastAPI()

app.include_router(root_router)

app.include_router(authRouter, prefix="/auth")
app.include_router(rootRouter)
app.include_router(adminRouter, prefix="/admin")
app.include_router(profileRouter, prefix="/profile")
app.include_router(articlesRouter, prefix="/articles")


# uvicorn.run(app, host="0.0.0.0", port=8000)

# You can start the server by running : uvicorn main:app --reload
# Or simply run the main.py file

