"""Local fork of render_excalidraw.py that sets ignore_https_errors=True on
the browser context — needed in this sandbox where the system trust store
rejects esm.sh's cert chain.

Usage: python render.py <input.excalidraw> [output.png]
"""

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def compute_bbox(elements):
    min_x = min_y = float("inf")
    max_x = max_y = float("-inf")
    for el in elements:
        if el.get("isDeleted"):
            continue
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0)
        h = el.get("height", 0)
        if el.get("type") in ("arrow", "line") and "points" in el:
            for px, py in el["points"]:
                min_x = min(min_x, x + px)
                min_y = min(min_y, y + py)
                max_x = max(max_x, x + px)
                max_y = max(max_y, y + py)
        else:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + abs(w))
            max_y = max(max_y, y + abs(h))
    if min_x == float("inf"):
        return 0, 0, 800, 600
    return min_x, min_y, max_x, max_y


def render(in_path: Path, out_path: Path, scale: int = 2, max_w: int = 2400):
    data = json.loads(in_path.read_text(encoding="utf-8"))
    elements = [e for e in data["elements"] if not e.get("isDeleted")]
    minx, miny, maxx, maxy = compute_bbox(elements)
    pad = 80
    vp_w = min(int(maxx - minx + pad * 2), max_w)
    vp_h = max(int(maxy - miny + pad * 2), 600)

    # Build template inline so we can pin the Excalidraw version (upstream
    # bundle for the latest tag has a broken transitive reference to
    # @braintree/sanitize-url@6.0.2 which 404s on esm.sh).
    local_template = Path(__file__).parent / "render_template.html"
    local_template.write_text(
        """<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<style>*{margin:0;padding:0;box-sizing:border-box;}body{background:#fff;overflow:hidden;}#root{display:inline-block;}#root svg{display:block;}</style>
</head><body>
<div id="root"></div>
<script type="module">
import { exportToSvg } from "https://esm.sh/@excalidraw/excalidraw@0.18.0?bundle";
window.renderDiagram = async function(jsonData){
  try {
    const data = typeof jsonData === "string" ? JSON.parse(jsonData) : jsonData;
    const svg = await exportToSvg({
      elements: data.elements || [],
      appState: { ...(data.appState||{}), exportBackground: true,
                  viewBackgroundColor: (data.appState||{}).viewBackgroundColor || "#ffffff",
                  exportWithDarkMode: false },
      files: data.files || {}
    });
    const root = document.getElementById("root");
    root.innerHTML = "";
    root.appendChild(svg);
    window.__renderComplete = true;
    return { success: true };
  } catch(e){
    window.__renderComplete = true;
    window.__renderError = e.message;
    return { success: false, error: e.message };
  }
};
window.__moduleReady = true;
</script>
</body></html>""",
        encoding="utf-8",
    )
    template_url = local_template.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--ignore-certificate-errors"],
        )
        context = browser.new_context(
            viewport={"width": vp_w, "height": vp_h},
            device_scale_factor=scale,
            ignore_https_errors=True,
        )
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(("pageerror", str(e))))
        page.on(
            "requestfailed",
            lambda r: errors.append(("requestfailed", r.url, str(r.failure))),
        )

        page.goto(template_url)
        try:
            page.wait_for_function("window.__moduleReady === true", timeout=45000)
        except Exception as e:
            print("Module did not become ready:", e, file=sys.stderr)
            for ev in errors:
                print("  ", ev, file=sys.stderr)
            browser.close()
            sys.exit(1)

        result = page.evaluate(
            "window.renderDiagram(%s)" % json.dumps(json.dumps(data))
        )
        if not result or not result.get("success"):
            print(
                "renderDiagram failed:",
                (result or {}).get("error", "no result"),
                file=sys.stderr,
            )
            browser.close()
            sys.exit(1)

        page.wait_for_function("window.__renderComplete === true", timeout=20000)
        svg = page.query_selector("#root svg")
        if svg is None:
            print("No SVG found", file=sys.stderr)
            browser.close()
            sys.exit(1)
        svg.screenshot(path=str(out_path))
        browser.close()


if __name__ == "__main__":
    in_p = Path(sys.argv[1])
    out_p = Path(sys.argv[2]) if len(sys.argv) > 2 else in_p.with_suffix(".png")
    render(in_p, out_p)
    print(f"Wrote {out_p}")
