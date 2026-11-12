# CLAUDE.md

## Project
Interactive, single-file HTML explainer of Feynman path integrals for an expert audience.
Main file: `feynman-path-integral.html`. Published as a claude.ai artifact:
https://claude.ai/artifact/Fhxf9ktuZdNxm4f4eh2r6e (private until shared from its Share menu).

## Structure of the page
Intro (time-sliced propagator) + five sections, each with prose, an interactive canvas figure,
a control panel (`.ctl`) and a readout grid (`.ro`):
1. Sum over paths as a phasor sum (Brownian-bridge samples, phase-colored)
2. Stationary phase, Cornu spiral, SPA vs numerical integral
3. Double slit + Aharonov–Bohm phase (paraxial free-propagator composition)
4. Euclidean path-integral Monte Carlo (Metropolis; harmonic / double well; exact ψ0, E0, E1 by inverse iteration)
5. Caustics, conjugate points, Morse/Maslov index (harmonic oscillator)

## Conventions
- **Language:** English is primary, Italian secondary. Toggle EN | IT in the header; choice stored in `localStorage` key `pi-lang`.
  - Markup: every text exists twice, `data-l="en"` and `data-l="it"` (CSS hides the inactive one).
  - `<option>`: `data-en` / `data-it` attributes, swapped by `setLang()`.
  - JS strings (readouts, canvas labels, buttons): `tr('English', 'Italiano')`.
  - Any new text must be added in both languages.
- **Style:** technical, minimal. IBM Plex Sans / IBM Plex Mono. Colors only via CSS tokens on `:root`
  (`--bg --panel --fg --muted --rule --grid --accent --hot --teal`), with dark-mode overrides; canvas reads them via `readPal()`.
- **Math:** MathJax 3.2.2 (SVG) from jsDelivr; `\( \)` inline, `\[ \]` display.
- **Units:** m = 1; §3 lengths in λ; §4–§5 ħ = ω = 1.
- **Artifact file format:** no `<!doctype>`, `<html>`, `<head>`, `<body>` (claude.ai adds the skeleton).
  `<title>`, `<style>` and scripts sit at the top of the file. A standalone copy for GitHub Pages needs that skeleton added.
- Physics first: every figure must be computed from the stated formulas, never faked.

## Workflow
- Check in a browser at desktop and phone width (~400 px), light and dark theme, both languages; no console errors, no horizontal scroll.
- Commit messages in English. Do not push to `main` directly; work on a branch and open a PR.
