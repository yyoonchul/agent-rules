Bundled runtime dependencies for `assignment-solver`.

- `pypdf==6.9.1` for `.pdf` text extraction
- `olefile==0.47` for opening legacy OLE `.ppt` files

These packages are vendored into the skill folder so the skill can read supported
lecture material formats without installing modules in each target project.

## Optional: page-level PDF OCR (`scripts/extract_pdf_page_ocr.py`)

The OCR helper is **not** bundled. It relies on **external** tools on the machine
that runs the script:

- **Tesseract** (`tesseract` on PATH). On macOS: `brew install tesseract tesseract-lang`
  (install language packs you need, e.g. Korean).
- **PDF → image** (one of):
  - **Poppler** (`pdftoppm` on PATH). On macOS: `brew install poppler`
  - **PyMuPDF** (`import fitz`) in the same Python environment, e.g. `pip install pymupdf`
    (use only if Poppler is unavailable; do not install into the target assignment
    project unless the user allows it).

If these are missing, the script exits with a clear error; the skill should surface
that message and avoid fabricating PDF content.
