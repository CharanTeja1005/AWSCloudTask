from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import files_route
from src.routes import operation_route
from src.routes import user_route

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(files_route.router)
app.include_router(operation_route.router)
app.include_router(user_route.router)
