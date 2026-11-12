# CLAUDE.md

## Project
Collection of interactive, single-file HTML physics explainers for an expert audience.
First artifact: `artifacts/feynman-path-integral.html`. Also published as a private claude.ai artifact
(working preview only): https://claude.ai/artifact/Fhxf9ktuZdNxm4f4eh2r6e
Second artifact: `artifacts/replica-symmetry-breaking.html` (Parisi RSB in the SK model; same conventions).
Popular companions: `artifacts/path-integrals-explained.html` (Feynman) and `artifacts/spin-glasses-explained.html`, (accessible language, "Example" and "In short" boxes, same rigor).

## Distribution
Public distribution is GitHub Pages, not claude.ai sharing.
- `artifacts/<slug>.html`: sources in claude.ai artifact format. `artifacts/manifest.json`: list that drives the index.
- `scripts/build.py` wraps each source into a full HTML document at `_site/<slug>/index.html`
  (adds doctype/head/body and a "← Index" link) and builds `_site/index.html` from `site/index.html`.
- `.github/workflows/pages.yml` builds and deploys on every push to `main`.
  URL: https://marcomauro.github.io/physics-artifact/ (one subfolder per slug).
- New artifact = new source file + manifest entry (`level`: `expert` or `popular`, shown as a badge in the index). Keep slugs stable: they are public URLs.
- `pi-lang` and `pi-theme` in `localStorage` are shared by all pages on the site; reuse them in new artifacts.

## Structure of the Feynman page
Intro (time-sliced propagator) + five sections, each with prose, an interactive canvas figure,
a control panel (`.ctl`) and a readout grid (`.ro`):
1. Sum over paths as a phasor sum (Brownian-bridge samples, phase-colored)
2. Stationary phase, Cornu spiral, SPA vs numerical integral
3. Double slit + Aharonov–Bohm phase (paraxial free-propagator composition)
4. Euclidean path-integral Monte Carlo (Metropolis; harmonic / double well; exact ψ0, E0, E1 by inverse iteration)
5. Caustics, conjugate points, Morse/Maslov index (harmonic oscillator)

## Conventions
- **Language:** English is primary, Italian secondary. Toggle EN | IT in the header; choice stored in `localStorage` key `pi-lang`.
- **Theme:** AUTO | ☀ | ☾ toggle in the header; `localStorage` key `pi-theme` (absent = follow system).
  - Markup: every text exists twice, `data-l="en"` and `data-l="it"` (CSS hides the inactive one).
  - `<option>`: `data-en` / `data-it` attributes, swapped by `setLang()`.
  - JS strings (readouts, canvas labels, buttons): `tr('English', 'Italiano')`.
  - Any new text must be added in both languages.
- **Style:** technical, minimal. IBM Plex Sans / IBM Plex Mono. Colors only via CSS tokens on `:root`
  (`--bg --panel --fg --muted --rule --grid --accent --hot --teal`), with dark-mode overrides; canvas reads them via `readPal()`.
- **Math:** MathJax 3.2.2 (SVG) from jsDelivr; `\( \)` inline, `\[ \]` display.
- **Units:** m = 1; §3 lengths in λ; §4–§5 ħ = ω = 1.
- **Artifact file format:** no `<!doctype>`, `<html>`, `<head>`, `<body>` (claude.ai adds the skeleton).
  `<title>`, `<meta>`, `<link>`, `<style>` and head scripts sit at the top of the file; `scripts/build.py` moves exactly
  that leading block into `<head>` for GitHub Pages.
- Physics first: every figure must be computed from the stated formulas, never faked.

## Workflow
- Check in a browser at desktop and phone width (~400 px), light and dark theme, both languages; no console errors, no horizontal scroll.
- Commit messages in English. Do not push to `main` directly; work on a branch and open a PR.
