from __future__ import annotations

import json

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import (
    render_docs,
    render_journeys,
    render_models,
    render_overview,
    render_warehouse,
)
from app.services.attribution_service import build_service

app = FastAPI(
    title="Attribution Warehouse Lab",
    version="0.1.0",
    description=(
        "Warehouse-oriented attribution lab for journey stitching, model comparison, "
        "weighted credit, and explainable channel allocation."
    ),
)

service = build_service()


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/journeys", response_class=HTMLResponse)
def journeys_page() -> str:
    return render_journeys()


@app.get("/models", response_class=HTMLResponse)
def models_page() -> str:
    return render_models()


@app.get("/warehouse", response_class=HTMLResponse)
def warehouse_page() -> str:
    return render_warehouse()


@app.get("/docs", response_class=HTMLResponse)
def docs_page() -> str:
    return render_docs()


@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return service.summary()


@app.get("/api/journeys")
def api_journeys() -> list[dict]:
    return service.journeys()


@app.get("/api/models")
def api_models() -> list[dict]:
    return service.models()


@app.get("/api/contracts")
def api_contracts() -> dict:
    return service.warehouse_contracts()


@app.get("/api/sample")
def api_sample() -> dict:
    return service.api_payload()


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    import os

    import uvicorn

    port = int(os.environ.get("PORT", "5034"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
