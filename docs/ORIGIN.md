# Why We Built This

Attribution discussions get distorted when the only visible layer is the chart.

Teams argue over sourced pipeline, assisted influence, paid versus organic, or whether a channel “really” created revenue, but the underlying warehouse logic is often hidden. That means people are debating conclusions without being able to inspect the journey rows, the conversion grain, or the credit model itself.

This repo exists to make that hidden layer visible.

The goal was not to build another BI clone. It was to build a compact warehouse-shaped artifact that shows three things clearly:

- how journeys are stitched
- how different models allocate credit
- how SQL and data contracts shape the result

That matters because attribution is rarely about discovering one perfect truth. It is about making tradeoffs explicit enough that marketing, RevOps, and leadership can choose a model deliberately instead of inheriting one by accident.

The design philosophy is straightforward:

- warehouse-first, because trustworthy attribution starts in the data model
- operator-legible, because non-data stakeholders still need to understand what is happening
- locally inspectable, because the repo should prove the logic without needing a giant platform stack
- recruiter-readable, because a strong data repo should still communicate value quickly

The sample journeys are intentionally varied across SaaS, industrial, healthcare, and fintech lanes. That keeps the repo from reading like a toy ad-tech example while still staying legible.

The SQL assets matter just as much as the Python service. Without visible staging, fact, and mart patterns, the project would collapse back into a dashboard story. Keeping those layers in the repo is what gives the attribution logic real structure.

This is the core idea behind `attribution-warehouse-lab`: attribution becomes more credible when the warehouse contract is part of the product surface, not buried behind it.
