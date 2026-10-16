"""Build a standalone copy of the portfolio for hosting on your own domain.

The published artifact's index.html is a page fragment (the artifact viewer adds the
<!doctype>, <head> and <body>). This wraps it in a full document, adds link-preview
metadata and a favicon, and copies the assets and resume next to it.

Usage:  python3 tools/build_site.py [domain]      (run from the portfolio folder)
Output: ../site/ and ../iliya-ghamoushi-site.zip
"""
import shutil
import sys
from pathlib import Path

DOMAIN = (sys.argv[1] if len(sys.argv) > 1 else "iliya-ghamoushi.com").lower()
HERE = Path(__file__).resolve().parent.parent          # portfolio/
OUT = HERE.parent / "site"
DESCRIPTION = ("Iliya Ghamoushi, mechatronics engineering student at McMaster University. "
               "Controls, embedded systems and design projects. Looking for a Summer 2027 internship.")

fragment = (HERE / "index.html").read_text(encoding="utf-8")
split = fragment.index("</style>") + len("</style>")
head_part, body_part = fragment[:split], fragment[split:]

favicon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' rx='12' fill='%231b6a45'/%3E"
           "%3Ctext x='32' y='42' text-anchor='middle' font-family='Arial,sans-serif' font-weight='700' "
           "font-size='28' fill='%23eef3ff'%3EIG%3C/text%3E%3C/svg%3E")

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{DESCRIPTION}">
<meta property="og:type" content="website">
<meta property="og:title" content="Iliya Ghamoushi">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="https://{DOMAIN}/">
<meta property="og:image" content="https://{DOMAIN}/assets/circuit-wide.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://{DOMAIN}/">
<link rel="icon" href="{favicon}">
<style>
:root {{ color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
body {{ margin: 0; font: 14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
</style>
{head_part.strip()}
</head>
<body>
{body_part.strip()}
</body>
</html>
"""

if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "assets").mkdir(parents=True)
(OUT / "index.html").write_text(page, encoding="utf-8")
for f in (HERE / "assets").iterdir():
    if f.is_file():
        shutil.copy2(f, OUT / "assets" / f.name)
shutil.copy2(HERE / "Iliya-Ghamoushi-Resume.pdf", OUT / "Iliya-Ghamoushi-Resume.pdf")
(OUT / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")   # used by GitHub Pages; ignored elsewhere

archive = shutil.make_archive(str(HERE.parent / "iliya-ghamoushi-site"), "zip", OUT)
print("built", OUT, "and", archive)
