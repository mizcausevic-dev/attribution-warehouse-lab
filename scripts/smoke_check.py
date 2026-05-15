from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app


def main() -> None:
    client = TestClient(app)
    checks = [
        "/",
        "/journeys",
        "/models",
        "/warehouse",
        "/docs",
        "/api/dashboard/summary",
        "/api/journeys",
        "/api/models",
        "/api/contracts",
        "/api/sample",
    ]
    for path in checks:
        response = client.get(path)
        assert response.status_code == 200, f"{path} returned {response.status_code}"
    print("smoke-ok")


if __name__ == "__main__":
    main()
