from __future__ import annotations

import html
import json
from pathlib import Path

from app.services.attribution_service import build_service


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


SERVICE = build_service()


def page_shell(title: str, kicker: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_escape(title)}</title>
  <style>
    :root {{
      --bg: #f4efe7;
      --ink: #1c1e26;
      --muted: #6d7585;
      --panel: #fffdf8;
      --line: #d9d3ca;
      --accent: #2d63ff;
      --accent-soft: #e7edff;
      --warm: #f2d8a7;
      --green: #1f8f63;
      --shadow: 0 22px 50px rgba(51, 45, 35, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Inter", "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at top right, rgba(45,99,255,0.09), transparent 26%),
        linear-gradient(180deg, #f7f1e7 0%, var(--bg) 100%);
      color: var(--ink);
    }}
    .page {{
      width: 1440px;
      min-height: 930px;
      margin: 0 auto;
      padding: 42px 48px 60px;
    }}
    .frame {{
      border: 1px solid var(--line);
      border-radius: 34px;
      background: rgba(255,253,248,0.92);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}
    .hero {{
      padding: 30px 34px 34px;
      background:
        radial-gradient(circle at top right, rgba(45,99,255,0.12), transparent 30%),
        linear-gradient(180deg, #fffdfa 0%, #f7f1e8 100%);
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.24em;
      font-weight: 800;
      margin-bottom: 14px;
    }}
    h1 {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 68px;
      line-height: 0.94;
      letter-spacing: -0.05em;
      max-width: 1040px;
    }}
    .lede {{
      margin-top: 18px;
      max-width: 900px;
      color: var(--muted);
      font-size: 19px;
      line-height: 1.6;
    }}
    .pill-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 24px;
    }}
    .pill {{
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid #c9d5ff;
      background: var(--accent-soft);
      color: #2346b7;
      font-size: 14px;
      font-weight: 700;
    }}
    .section {{
      padding: 28px 32px 34px;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
    }}
    .stat {{
      padding: 22px;
      border-radius: 24px;
      border: 1px solid var(--line);
      background: var(--panel);
      min-height: 172px;
    }}
    .stat .label {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-weight: 700;
      margin-bottom: 14px;
    }}
    .stat .value {{
      font-family: Georgia, "Times New Roman", serif;
      font-size: 54px;
      line-height: 0.92;
      margin-bottom: 12px;
    }}
    .stat .copy {{
      color: #505867;
      font-size: 15px;
      line-height: 1.55;
    }}
    .banner {{
      margin-top: 24px;
      padding: 18px 22px;
      border-radius: 22px;
      border: 1px solid #ccd8ff;
      background: linear-gradient(90deg, rgba(45,99,255,0.09), rgba(45,99,255,0.03));
      color: #2748b2;
      font-size: 16px;
      line-height: 1.55;
      font-weight: 600;
    }}
    .grid {{
      display: grid;
      gap: 18px;
      grid-template-columns: repeat(3, 1fr);
      margin-top: 24px;
    }}
    .card {{
      border-radius: 24px;
      border: 1px solid var(--line);
      background: var(--panel);
      padding: 22px;
      min-height: 250px;
    }}
    .card .kicker {{
      color: var(--accent);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-weight: 800;
      margin-bottom: 18px;
    }}
    .card h2 {{
      margin: 0 0 14px;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 28px;
      line-height: 1.05;
      letter-spacing: -0.03em;
    }}
    .card p, .card li {{
      margin: 0;
      color: #596171;
      font-size: 15px;
      line-height: 1.58;
    }}
    .card ul {{
      margin: 0;
      padding-left: 18px;
    }}
    .footer-note {{
      margin-top: 16px;
      padding-top: 14px;
      border-top: 1px solid #ebe3d7;
      color: #3c4658;
      font-size: 14px;
    }}
    .table-shell {{
      margin-top: 24px;
      overflow: hidden;
      border-radius: 24px;
      border: 1px solid var(--line);
      background: var(--panel);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      padding: 16px 18px;
      text-align: left;
      vertical-align: top;
    }}
    thead th {{
      background: #f8f3eb;
      color: var(--muted);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      font-weight: 800;
    }}
    tbody tr + tr td {{
      border-top: 1px solid #ede7de;
    }}
    .mono {{
      font-family: Consolas, "SFMono-Regular", monospace;
      font-size: 13px;
    }}
    .sql-panel {{
      margin-top: 24px;
      border-radius: 22px;
      border: 1px solid #22314d;
      background: #121828;
      color: #d9e5ff;
      padding: 22px;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: Consolas, "SFMono-Regular", monospace;
      font-size: 14px;
      line-height: 1.5;
    }}
    .two-col {{
      display: grid;
      gap: 18px;
      grid-template-columns: 1.1fr 0.9fr;
      margin-top: 24px;
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="frame">
      <div class="hero">
        <div class="eyebrow">{_escape(kicker)}</div>
        {body}
      </div>
    </div>
  </div>
</body>
</html>"""


def render_overview() -> str:
    summary = SERVICE.summary()
    models = SERVICE.models()
    body = f"""
      <h1>Warehouse-first attribution that leadership can actually interrogate.</h1>
      <p class="lede">
        Attribution Warehouse Lab stitches journey touchpoints, compares competing
        allocation models, and publishes the SQL contract layer so sourced pipeline,
        influenced revenue, and weighted credit can all be reviewed from the same system.
      </p>
      <div class="pill-row">
        <div class="pill">journey stitching</div>
        <div class="pill">first / last / linear / weighted</div>
        <div class="pill">channel credit mart</div>
        <div class="pill">warehouse contracts</div>
      </div>
      <div class="section">
        <div class="stats">
          <div class="stat"><div class="label">Journeys</div><div class="value">{summary['journeyCount']}</div><div class="copy">Attributed account journeys that actually converted instead of generic web analytics traffic.</div></div>
          <div class="stat"><div class="label">Channels</div><div class="value">{summary['channelCount']}</div><div class="copy">Distinct sources competing for credit across the modeled warehouse journeys.</div></div>
          <div class="stat"><div class="label">Touches</div><div class="value">{summary['touchCount']}</div><div class="copy">Individual touchpoints stitched into end-to-end account narratives.</div></div>
          <div class="stat"><div class="label">Pipeline</div><div class="value">${summary['pipelineDollars']:,}</div><div class="copy">Total attributable pipeline carried through the sample warehouse fact layer.</div></div>
        </div>
        <div class="banner">{_escape(summary['leadRecommendation'])}</div>
        <div class="grid">
          {''.join(
              f'''<div class="card"><div class="kicker">{_escape(model["label"])}</div><h2>{_escape(model["description"])}</h2><p>The same journey set can tell four different budget stories. This repo makes that contrast explicit instead of burying it in slideware.</p><div class="footer-note">Top channel: {_escape(model["credits"][0]["channel"])} · Allocated pipeline ${model["credits"][0]["allocatedPipeline"]:,.0f}</div></div>'''
              for model in models
          )}
        </div>
      </div>
    """
    return page_shell("Attribution Warehouse Lab - Overview", "attribution warehouse lab", body)


def render_journeys() -> str:
    journeys = SERVICE.journeys()
    rows = []
    for journey in journeys:
        touch_summary = " → ".join(touch["channel"] for touch in journey["touches"])
        rows.append(
            f"""
            <tr>
              <td><strong>{_escape(journey["account"])}</strong><div class="footer-note">{_escape(journey["journeyId"])} · {_escape(journey["segment"])}</div></td>
              <td>{_escape(journey["conversionType"])}</td>
              <td class="mono">{_escape(touch_summary)}</td>
              <td>${journey["pipelineDollars"]:,}</td>
              <td>{journey["daysToConvert"]} days</td>
            </tr>
            """
        )
    body = f"""
      <h1>Journey stitching is where attribution becomes explainable.</h1>
      <p class="lede">
        A warehouse model is only useful if the underlying journey rows are legible.
        This lane shows how touches roll into account conversion stories before any model gets to claim victory.
      </p>
      <div class="section">
        <div class="table-shell">
          <table>
            <thead>
              <tr>
                <th>Account</th>
                <th>Conversion</th>
                <th>Touch path</th>
                <th>Pipeline</th>
                <th>Time to convert</th>
              </tr>
            </thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </div>
        <div class="grid">
          {''.join(
              f'''<div class="card"><div class="kicker">{_escape(journey["account"])}</div><h2>{_escape(journey["conversionType"])}</h2><ul>{''.join(f"<li>{_escape(touch['channel'])}: {_escape(touch['campaign'])}</li>" for touch in journey["touches"])}</ul><div class="footer-note">Segment: {_escape(journey["segment"])} · Pipeline ${journey["pipelineDollars"]:,}</div></div>'''
              for journey in journeys[:3]
          )}
        </div>
      </div>
    """
    return page_shell("Attribution Warehouse Lab - Journeys", "journey stitching", body)


def render_models() -> str:
    models = SERVICE.models()
    body = f"""
      <h1>Different models tell different revenue stories on the same warehouse rows.</h1>
      <p class="lede">
        The point of attribution is not to find one magical truth. It is to make the tradeoffs obvious enough that RevOps, demand gen, and leadership can choose the right lens consciously.
      </p>
      <div class="section">
        <div class="grid">
          {''.join(
              f'''<div class="card"><div class="kicker">{_escape(model["label"])}</div><h2>{_escape(model["description"])}</h2><ul>{''.join(f"<li>{_escape(row['channel'])}: ${row['allocatedPipeline']:,.0f} pipeline · ROI {row['roiRatio'] if row['roiRatio'] is not None else 'n/a'}</li>" for row in model["credits"][:3])}</ul><div class="footer-note">Model name: {_escape(model["name"])}</div></div>'''
              for model in models
          )}
        </div>
      </div>
    """
    return page_shell("Attribution Warehouse Lab - Models", "model comparison", body)


def render_warehouse() -> str:
    contracts = SERVICE.warehouse_contracts()
    sql_preview = "\n\n".join(
        f"-- {asset['name']}\n{asset['sql']}" for asset in contracts["sqlAssets"]
    )
    body = f"""
      <h1>Warehouse contracts matter as much as the credit model.</h1>
      <p class="lede">
        If the staging grain, fact grain, and mart grain are fuzzy, the attribution model is just decoration. This page keeps the actual warehouse contract visible.
      </p>
      <div class="section">
        <div class="two-col">
          <div class="grid" style="margin-top: 0; grid-template-columns: 1fr;">
            {''.join(
                f'''<div class="card" style="min-height: 0;"><div class="kicker">{_escape(item["name"])}</div><h2>{_escape(item["grain"])}</h2><p>{_escape(item["contract"])}</p></div>'''
                for item in contracts["datasets"]
            )}
          </div>
          <div class="sql-panel"><pre>{_escape(sql_preview)}</pre></div>
        </div>
      </div>
    """
    return page_shell("Attribution Warehouse Lab - Warehouse", "warehouse contracts", body)


def render_docs() -> str:
    payload = SERVICE.api_payload()
    body = f"""
      <h1>A local-first attribution lab with real warehouse shape.</h1>
      <p class="lede">
        This repo is intentionally small, but it still shows the important parts:
        journey stitching, model comparison, warehouse contracts, SQL assets, and an API layer that makes the lab inspectable instead of ornamental.
      </p>
      <div class="section">
        <div class="two-col">
          <div class="grid" style="margin-top: 0; grid-template-columns: 1fr;">
            <div class="card" style="min-height: 0;"><div class="kicker">What it proves</div><h2>Analytics depth without a giant stack.</h2><p>Useful enough for recruiter scans, but still anchored in real data-modeling concerns that warehouse teams actually care about.</p></div>
            <div class="card" style="min-height: 0;"><div class="kicker">Routes</div><h2>Journeys, models, contracts, and summary APIs.</h2><p>`/api/journeys`, `/api/models`, `/api/contracts`, and `/api/sample` are enough to demonstrate the full warehouse story.</p></div>
          </div>
          <div class="sql-panel"><pre>{_escape(json.dumps(payload, indent=2))}</pre></div>
        </div>
      </div>
    """
    return page_shell("Attribution Warehouse Lab - Docs", "implementation notes", body)


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-journeys.html": render_journeys(),
        "03-models.html": render_models(),
        "04-warehouse.html": render_warehouse(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        target = output_dir / name
        target.write_text(contents, encoding="utf-8")
        written.append(target)
    return written
