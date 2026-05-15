from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.attribution_service import build_service


class AttributionWarehouseLabTests(unittest.TestCase):
    def test_summary_shape(self) -> None:
        summary = build_service().summary()
        self.assertEqual(summary["journeyCount"], 4)
        self.assertGreater(summary["pipelineDollars"], 0)

    def test_position_weighted_has_top_channel(self) -> None:
        model = next(item for item in build_service().models() if item["name"] == "position_weighted")
        self.assertGreater(len(model["credits"]), 0)
        self.assertIn("channel", model["credits"][0])

    def test_contracts_api(self) -> None:
        client = TestClient(app)
        response = client.get("/api/contracts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["sqlAssets"]), 3)


if __name__ == "__main__":
    unittest.main()
