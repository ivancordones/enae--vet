from fastapi import FastAPI


app = FastAPI(title="ENAE VET API", version="0.1.0")


@app.get("/health", tags=["internal"])
def read_health() -> dict[str, str]:
    """Simple health endpoint for smoke tests and readiness checks."""
    return {"status": "ok"}


@app.get("/", tags=["internal"])
def read_root() -> dict[str, str]:
    """Root endpoint returning a minimal greeting."""
    return {"message": "ENAE VET backend skeleton (SCRUM-5)."}

