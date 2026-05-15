from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.render import write_static_proof_pages


OUT_DIR = ROOT / "screenshots"
OUT_DIR.mkdir(exist_ok=True)


def _edge_path() -> Path:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Microsoft Edge not found")


def main() -> None:
    for item in OUT_DIR.glob("*"):
      if item.is_file():
        item.unlink()
    pages = write_static_proof_pages(OUT_DIR)
    browser = _edge_path()
    for page in pages:
        png_path = page.with_suffix(".png")
        command = [
            str(browser),
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1600,1000",
            "--virtual-time-budget=4000",
            f"--screenshot={png_path}",
            page.resolve().as_uri(),
        ]
        result = shutil.which(str(browser))
        if result is None:
            raise FileNotFoundError(browser)
        import subprocess
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("rendered")


if __name__ == "__main__":
    main()
