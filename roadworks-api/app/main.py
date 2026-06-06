from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.exceptions import setup_exception_handlers
from app.api.router import api_router
from app.db.session import engine
from app.db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if not using alembic
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for Indian Road Construction Contractor Management System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
setup_exception_handlers(app)

# Routers
app.include_router(api_router, prefix="/api")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME, "version": "1.0.0"}
