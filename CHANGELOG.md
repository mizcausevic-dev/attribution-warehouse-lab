# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-05-15

### Released
- Published **attribution-warehouse-lab** as a public Python and FastAPI project for journey stitching, channel-credit model comparison, and warehouse-visible attribution logic.
- Packaged sample data, SQL assets, HTML proof surfaces, JSON APIs, validation scripts, screenshots, and CI into a recruiter- and buyer-readable repo.
- Clarified the real problem the repo addresses: attribution debate without inspectable warehouse contracts.

### Why this mattered
- Many attribution tools emphasize dashboards and executive summaries while leaving the warehouse layer opaque.
- This release made the underlying journey and SQL logic visible enough to review, not just the final charts.

## [0.1.0] - 2026-02-21

### Shipped
- Cut the first coherent internal version of the project with stable journey objects, model comparisons, and contract-level outputs.
- Locked the architecture around a small Python service plus visible SQL assets instead of overbuilding the stack.

## [Prototype] - 2025-08-04

### Built
- Built the first runnable prototype to test whether warehouse-shaped attribution proof would be more persuasive than another executive dashboard alone.
- Validated the concept against recurring pain points like sourced-vs-influenced disputes, inconsistent touchpoint grain, and channel ROI storytelling drift.

## [Design Phase] - 2024-10-17

### Designed
- Defined the system around warehouse visibility first and presentation second.
- Chose journey rows, conversion facts, and model allocation outputs as the core evidence lanes.

## [Idea Origin] - 2023-06-28

### Observed
- The original idea surfaced while looking at how often attribution conversations became strategic arguments built on weak or hidden data contracts.
- The recurring pattern was that teams needed more inspectable structure, not just better slides.

## [Background Signals] - 2022-09-12

### Context
- Earlier analytics and operations work made one pattern obvious: reporting only becomes trusted when the transformation and reconciliation layers are legible enough to challenge.
- That pattern shaped the thinking behind this repo well before the public version existed.
