# physics-artifact

Interactive physics explainers (EN / IT) that run entirely in the browser.

| Artifact | Source |
|---|---|
| Feynman Path Integrals | `artifacts/feynman-path-integral.html` |

## Layout

```
artifacts/
  manifest.json              list of artifacts (slug, titles, summaries, date) — drives the index
  <slug>.html                one self-contained page per artifact (claude.ai artifact format)
site/
  index.html                 template of the index page (cards are inserted at <!-- ARTIFACTS -->)
scripts/build.py             wraps each artifact into a full HTML document and builds the index
.github/workflows/pages.yml  builds and deploys to GitHub Pages on every push to main
```

The built site (`_site/`, not committed) has a stable URL per artifact:
`https://marcomauro.github.io/physics-artifact/<slug>/`, with the index at the root.

## Preview locally

```sh
python3 scripts/build.py
python3 -m http.server -d _site 8000   # http://localhost:8000
```

## Add an artifact

1. Put the page in `artifacts/<slug>.html` (no `<!doctype>`/`<html>`/`<head>`/`<body>`; the build adds them).
2. Add an entry to `artifacts/manifest.json`.
3. Run the build, check it, open a PR; merging to `main` publishes it.
