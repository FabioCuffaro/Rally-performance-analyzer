"""Rally Performance Analyzer — FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import rally, stages, drivers

app = FastAPI(
    title="Rally Performance Analyzer",
    description="API para analizar datos del World Rally Championship.",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(rally.router)
app.include_router(stages.router)
app.include_router(drivers.router)


@app.get("/health", tags=["Status"])
def health_check() -> dict:
    """Endpoint de salud — confirma que la API está en marcha."""
    return {"status": "ok", "service": "rally-performance-analyzer"}
