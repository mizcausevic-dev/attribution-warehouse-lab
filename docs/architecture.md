# Architecture

## Goal

`attribution-warehouse-lab` is a Python and FastAPI project for showing how attribution becomes more trustworthy when the warehouse layer is visible.

It focuses on the parts growth teams usually debate but rarely expose clearly:

- touchpoint journey stitching
- conversion-level fact rows
- competing channel-credit models
- warehouse grain contracts
- SQL assets that can actually be reviewed

## Service shape

The repo is intentionally small and local-first:

- `app/main.py` exposes HTML proof routes and JSON API routes.
- `app/services/attribution_service.py` loads sample journey data, computes model allocations, and exposes warehouse contract views.
- `app/render.py` turns the same service state into browsable proof surfaces.
- `warehouse/models/` carries sample SQL for staging, fact, and mart layers.
- `scripts/run_demo.py`, `scripts/smoke_check.py`, and `scripts/render_readme_assets.py` provide validation and screenshot generation.

## Data model

The current sample dataset contains:

- journey identity
- account and segment
- ordered touchpoints
- channel, campaign, stage, and touch cost
- conversion type
- pipeline dollars
- days to convert

The service computes:

- first-touch allocations
- last-touch allocations
- linear allocations
- position-weighted allocations

## Why it matters

Attribution arguments often happen at the presentation layer. The real issue is usually one layer deeper:

- unclear journey stitching
- fuzzy grain
- opaque credit logic
- no inspectable contract for how the model was built

That is the layer this repo is modeling.
