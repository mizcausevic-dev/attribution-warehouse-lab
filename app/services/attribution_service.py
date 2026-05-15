from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_attribution_data.json"
WAREHOUSE_DIR = Path(__file__).resolve().parents[2] / "warehouse" / "models"


@dataclass(slots=True)
class AttributionWarehouseService:
    source_path: Path
    warehouse_dir: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def journeys(self) -> list[dict[str, Any]]:
        data = self.load()
        return data["journeys"]

    def summary(self) -> dict[str, Any]:
        journeys = self.journeys()
        total_pipeline = sum(journey["pipelineDollars"] for journey in journeys)
        total_touches = sum(len(journey["touches"]) for journey in journeys)
        avg_days = round(mean(journey["daysToConvert"] for journey in journeys), 1)
        channels = sorted({touch["channel"] for journey in journeys for touch in journey["touches"]})
        return {
            "journeyCount": len(journeys),
            "channelCount": len(channels),
            "touchCount": total_touches,
            "pipelineDollars": total_pipeline,
            "averageDaysToConvert": avg_days,
            "leadRecommendation": (
                "Use the warehouse view to reconcile sourced, influenced, and weighted credit "
                "before leadership locks budget on a single attribution story."
            ),
        }

    def models(self) -> list[dict[str, Any]]:
        data = self.load()
        rows = []
        for model in data["models"]:
            rows.append(
                {
                    **model,
                    "credits": self._channel_credit(model["name"]),
                }
            )
        return rows

    def warehouse_contracts(self) -> dict[str, Any]:
        sql_assets = []
        for path in sorted(self.warehouse_dir.glob("*.sql")):
            sql_assets.append(
                {
                    "name": path.name,
                    "sql": path.read_text(encoding="utf-8"),
                }
            )
        return {
            "datasets": [
                {
                    "name": "stg_touchpoints",
                    "grain": "one row per attributable touchpoint",
                    "contract": "journey_id, touch_timestamp, channel, campaign, stage, touch_cost",
                },
                {
                    "name": "fct_attribution_journeys",
                    "grain": "one row per converted account journey",
                    "contract": "journey_id, account, segment, conversion_type, pipeline_dollars, days_to_convert",
                },
                {
                    "name": "mart_channel_credit",
                    "grain": "one row per channel per model",
                    "contract": "model_name, channel, allocated_pipeline, allocated_cost, roi_ratio",
                }
            ],
            "sqlAssets": sql_assets,
        }

    def api_payload(self) -> dict[str, Any]:
        models = self.models()
        return {
            "dashboard": self.summary(),
            "topJourney": self.journeys()[0],
            "topModel": {
                "name": models[3]["name"],
                "label": models[3]["label"],
                "credits": models[3]["credits"],
            },
        }

    def _channel_credit(self, model_name: str) -> list[dict[str, Any]]:
        totals: dict[str, dict[str, float]] = {}
        for journey in self.journeys():
            allocations = self._journey_allocations(journey, model_name)
            for channel, credit_share in allocations:
                row = totals.setdefault(channel, {"pipeline": 0.0, "cost": 0.0})
                row["pipeline"] += journey["pipelineDollars"] * credit_share
            for touch in journey["touches"]:
                row = totals.setdefault(touch["channel"], {"pipeline": 0.0, "cost": 0.0})
                row["cost"] += touch["cost"]

        rows = []
        for channel, values in totals.items():
            cost = round(values["cost"], 2)
            pipeline = round(values["pipeline"], 2)
            roi = round(pipeline / cost, 2) if cost else None
            rows.append(
                {
                    "channel": channel,
                    "allocatedPipeline": pipeline,
                    "allocatedCost": cost,
                    "roiRatio": roi,
                }
            )
        return sorted(rows, key=lambda row: row["allocatedPipeline"], reverse=True)

    def _journey_allocations(self, journey: dict[str, Any], model_name: str) -> list[tuple[str, float]]:
        touches = journey["touches"]
        if model_name == "first_touch":
            return [(touches[0]["channel"], 1.0)]
        if model_name == "last_touch":
            return [(touches[-1]["channel"], 1.0)]
        if model_name == "linear":
            share = 1 / len(touches)
            return [(touch["channel"], share) for touch in touches]
        if model_name == "position_weighted":
            if len(touches) == 1:
                return [(touches[0]["channel"], 1.0)]
            if len(touches) == 2:
                return [(touches[0]["channel"], 0.5), (touches[1]["channel"], 0.5)]
            middle_share = 0.2 / (len(touches) - 2)
            allocations = [(touches[0]["channel"], 0.4)]
            for touch in touches[1:-1]:
                allocations.append((touch["channel"], middle_share))
            allocations.append((touches[-1]["channel"], 0.4))
            return allocations
        raise KeyError(model_name)


def build_service(root: Path | None = None) -> AttributionWarehouseService:
    base = root or Path(__file__).resolve().parents[2]
    return AttributionWarehouseService(
        base / "app" / "data" / "sample_attribution_data.json",
        base / "warehouse" / "models",
    )
