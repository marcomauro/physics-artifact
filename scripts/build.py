#!/usr/bin/env python3
"""Build the static site for GitHub Pages.

Sources (artifacts/*.html) stay in claude.ai artifact format: no <!doctype>, <html>,
<head> or <body>. This script wraps each one into a complete HTML document and
generates the index page from artifacts/manifest.json.

    python3 scripts/build.py            # writes _site/
    python3 -m http.server -d _site     # preview at http://localhost:8000

Output layout:
    _site/index.html                    index of all artifacts
    _site/<slug>/index.html             one standalone page per artifact
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "artifacts"
SITE = ROOT / "site"
OUT = ROOT / "_site"

# Tags that belong in <head> when they lead the artifact file.
HEAD_TAG = re.compile(
    r"""\s*(?:
        <!--.*?-->
      | <title\b[^>]*>.*?</title>
      | <style\b[^>]*>.*?</style>
      | <script\b[^>]*>.*?</script>
      | <(?:meta|link|base)\b[^>]*>
    )""",
    re.S | re.I | re.X,
)

BACK_LINK = (
    '<nav class="site-back" style="max-width:1160px;margin:0 auto 12px;font:12px ui-monospace,SFMono-Regular,Menlo,monospace">'
    '<a href="../" style="color:inherit;opacity:.65;text-decoration:none">'
    '← Index</a></nav>\n'
)


def split_head(src: str) -> tuple[str, str]:
    """Split the leading head-type elements from the body content."""
    pos = 0
    while m := HEAD_TAG.match(src, pos):
        pos = m.end()
    return src[:pos].strip(), src[pos:].lstrip("\n")


def wrap(src: str, lang: str = "en") -> str:
    if re.match(r"\s*<!doctype", src, re.I):
        return src  # already a full document
    head, body = split_head(src)
    # claude.ai-only hint; the viewport meta below covers it.
    head = re.sub(r'\s*<meta name="claude:[^"]*"[^>]*>', "", head)
    return (
        f'<!doctype html>\n<html lang="{lang}">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f"{head}\n</head>\n<body>\n{BACK_LINK}{body.rstrip()}\n</body>\n</html>\n"
    )


def card(a: dict) -> str:
    e = lambda s: html.escape(s, quote=True)
    t, s = a["title"], a["summary"]
    return (
        f'    <li class="card"><a href="{e(a["slug"])}/">\n'
        f'      <h2><span data-l="en">{e(t["en"])}</span><span data-l="it">{e(t["it"])}</span></h2>\n'
        f'      <p><span data-l="en">{e(s["en"])}</span><span data-l="it">{e(s["it"])}</span></p>\n'
        f'      <span class="meta">{e(a.get("updated", ""))}<br><span class="go">'
        f'<span data-l="en">open →</span><span data-l="it">apri →</span></span></span>\n'
        "    </a></li>"
    )


def main() -> int:
    manifest = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    slugs = set()
    for a in manifest:
        slug = a["slug"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug) or slug in slugs:
            sys.exit(f"bad or duplicate slug: {slug!r}")
        slugs.add(slug)
        src = (SRC / a["source"]).read_text(encoding="utf-8")
        dest = OUT / slug / "index.html"
        dest.parent.mkdir(parents=True)
        dest.write_text(wrap(src), encoding="utf-8")
        print(f"  {a['source']} -> {dest.relative_to(ROOT)}")

    for f in SITE.iterdir():
        if f.name != "index.html" and f.is_file():
            shutil.copy2(f, OUT / f.name)
    index = (SITE / "index.html").read_text(encoding="utf-8")
    index = index.replace("<!-- ARTIFACTS -->", "\n".join(card(a) for a in manifest))
    (OUT / "index.html").write_text(index, encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print(f"  index with {len(manifest)} artifact(s) -> _site/index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
