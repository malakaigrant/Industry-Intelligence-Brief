# Fieldnote — Industry Intelligence

A PDF-first website that turns company and industry-report inputs into a ten-point industry intelligence brief.

## Start locally

No npm installation or build step is required. From this repository folder:

```sh
python -m http.server 4173 --directory dist
```

Open **http://localhost:4173**. Use an HTTP server rather than double-clicking `index.html`, because PDF loading uses JavaScript modules and fetch.

1. Select **Build an industry intelligence brief**.
2. Choose **Load Starbucks PDF**, or enter another company and upload relevant reports.
3. Download the complete PDF. Markdown is shown only after typing **Show markdown** or **Print in chat**.

## Upload to GitHub

1. Unzip the download and open the `fieldnote` folder.
2. Create an empty GitHub repository.
3. Upload the folder's **contents**, preserving `dist`, `pipeline`, and `.github/workflows`.
4. Commit the files to the `main` branch.
5. To host with GitHub Pages, open **Settings → Pages**, set **Source** to **GitHub Actions**, then run **Deploy Fieldnote to GitHub Pages** from the Actions tab (or push another commit to `main`).

The included workflow publishes `dist` directly. All local asset paths are relative, so GitHub project URLs work. GitHub Pages availability for private repositories depends on your GitHub plan and settings.

**Report access:** this package includes your supplied IBISWorld PDF and a derived brief. Keep the repository and hosting access private unless your report license permits redistribution. GitHub Pages can be publicly accessible even when its repository is private; check the audience before publishing.

## What works without an API key

The Starbucks route loads the included report and serves the completed, source-checked eight-page PDF. This brief was compiled in Python during development. Clicking the website button **does not run Python again**; it retrieves the compiled document. The brief is scoped to U.S. coffee and snack shop operations and the June 2026 report edition.

The built-in PDF includes:

- All ten requested numbered sections.
- Official 2022 Census NAICS comparison: 722515 versus 722513.
- Exact printed-page references and specific chart/table names.
- Separate historical estimates and forecasts, with CAGR calculations.
- Reported competitor share ranges without invented rankings.
- Information gaps, interpretations and a verification checklist.

## Live analysis of uploaded reports

The analyst enters an OpenAI API key in the form. The website extracts PDF text in the browser with PDF.js and sends it **directly to OpenAI's Responses API**. The key stays in page memory, is not written to browser storage, and is cleared from the form after success. No shared secret is embedded in the code. Never put an API key into this repository.

The API currently uses `gpt-4.1`, structured JSON responses and `store: false`. Each analysis makes two calls: draft and evidence audit. API billing applies to the analyst's key; a ChatGPT subscription does not itself configure this website's API access.

Limits: 3 reports, 20 MB per file, 200 pages total, 500,000 extracted characters. Image-only scans need OCR first. Report text is treated as evidence, never instructions. Unsupported claims are omitted or labeled unverified. Exact supporting excerpts are checked against extracted page text; a second model pass checks claims, figures and citation labels. These checks reduce errors but are not a guarantee of factual correctness.

For arbitrary industries, official Census descriptions are **not fetched automatically**. Unless verified definitions and company activity are present in supplied documents, the NAICS selection is flagged for human review. The Starbucks comparison was independently checked during development.

The custom-upload path generates PDFs in JavaScript with jsPDF. It does not use a Python/Code Interpreter service. A future shared-service deployment should move API credentials and calls to a server; this version deliberately supports analyst-owned keys for a static site.

## Files

```text
dist/
  index.html               Website layout
  style.css                Responsive styling
  app.js                   Intake, PDF loading, analysis, validation and export
  starbucks-source.pdf     Supplied IBISWorld report
  starbucks-brief.pdf       Compiled eight-page brief
  starbucks-brief.json      Structured brief; used for explicit Markdown requests
  vendor/                  Pinned PDF.js and jsPDF browser libraries
pipeline/
  build_brief.py           Python source for the built-in brief
.github/workflows/
  deploy.yml               GitHub Pages deployment
requirements.txt           Python PDF-builder dependencies
```

## Rebuild the built-in PDF

```sh
python -m pip install -r requirements.txt
python pipeline/build_brief.py
```

The script writes the PDF to `outputs/` and copies the website copy and JSON to `dist/`. Its source-checked findings are explicitly authored in the script; it is not a universal report extraction model. To update the report edition, update and verify the findings, citations, calculations and source PDF, then rebuild. Review the generated PDF visually before publishing.

## Validation performed

- Confirmed the required starter and the Starbucks completion state in the browser.
- Confirmed no full brief appears by default; explicit `Show markdown` reveals it.
- Recomputed CAGR values and checked competitor bands against the supplied report.
- Rendered and visually inspected the built-in PDF.
- Checked JavaScript syntax and packaged asset references.

**Not yet exercised:** an end-to-end live OpenAI analysis with a working API key. No key was supplied during development. GitHub Pages deployment also must be run in your repository.
