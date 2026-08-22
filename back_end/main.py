from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401 - garante que os models sejam registrados no metadata
from app.api.alunosController import router as alunos_router
from app.api.responsaveisController import router as responsaveis_router
from app.api.salasController import router as salas_router
from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Escola API", lifespan=lifespan)

app.include_router(salas_router)
app.include_router(alunos_router)
app.include_router(responsaveis_router)
