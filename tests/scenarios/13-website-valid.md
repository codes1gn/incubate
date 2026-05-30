# Scenario 13 — website-valid

**What it validates:** The GitHub Pages site is valid HTML with required design elements and CI workflows are present.

## Requirements
- `docs/index.html` exists and is valid HTML
- Dark terminal aesthetic (#0d1117 background)
- Stats/metrics visible on the page
- `.github/workflows/pages.yml` exists (GitHub Pages deployment)
- `.github/workflows/tests.yml` exists (CI test runner)

## Checks
- `docs/index.html` exists
- Valid HTML structure (`<!DOCTYPE html>` or `<html>`)
- `<title>` tag is present
- Dark background color is set
- Stats or metrics are shown on page
- `pages.yml` workflow exists
- `tests.yml` workflow exists
