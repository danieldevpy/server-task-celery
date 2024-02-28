from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from glpi.route import router as routerGLPI
from sso.route import router as routerSSO

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routerGLPI)
app.include_router(routerSSO)

