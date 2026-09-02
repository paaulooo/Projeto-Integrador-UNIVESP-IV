from contextlib import asynccontextmanager

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app import models  # noqa: F401 - garante que os models sejam registrados no metadata
from app.api.alunosController import router as alunos_router
from app.api.responsaveisController import router as responsaveis_router
from app.api.salasController import router as salas_router
from app.database import Base, engine

load_dotenv()

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Escola API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(salas_router)
app.include_router(alunos_router)
app.include_router(responsaveis_router)


