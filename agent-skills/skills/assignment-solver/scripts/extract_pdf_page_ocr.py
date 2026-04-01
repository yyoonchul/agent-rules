#!/usr/bin/env python3
"""
Page-level OCR for PDF files using external tools (not bundled).

Rendering (first match wins):
  - Poppler: pdftoppm on PATH
  - Optional: PyMuPDF (fitz) if importable in the current Python environment

OCR:
  - Tesseract CLI on PATH

This script is intentionally separate from extract_reference_text.py so agents
can invoke it only when text extraction is insufficient.
"""
from __future__ import annotations

import argparse
import glob
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_page_spec(spec: str) -> list[int]:
    """Parse '1,3-5,7' into sorted unique 1-based page numbers."""
    result: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                start = int(a.strip())
                end = int(b.strip())
            except ValueError as exc:
                raise ValueError(f"invalid page range: {part!r}") from exc
            if start < 1 or end < 1:
                raise ValueError("page numbers must be >= 1")
            if start > end:
                start, end = end, start
            for p in range(start, end + 1):
                result.add(p)
        else:
            try:
                n = int(part)
            except ValueError as exc:
                raise ValueError(f"invalid page number: {part!r}") from exc
            if n < 1:
                raise ValueError("page numbers must be >= 1")
            result.add(n)
    return sorted(result)


def pdf_page_count(pdf_path: Path) -> int:
    """Return number of pages using bundled pypdf (same skill vendor)."""
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    vendor_dir = skill_dir / "vendor"
    if str(vendor_dir) not in sys.path:
        sys.path.insert(0, str(vendor_dir))
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(pdf_path))
    return len(reader.pages)


def find_executable(name: str) -> str | None:
    return shutil.which(name)


def render_page_pdftoppm(pdf_path: Path, page_1based: int, out_png: Path) -> None:
    """Render one page to PNG via pdftoppm -singlefile."""
    pdftoppm = find_executable("pdftoppm")
    if not pdftoppm:
        raise RuntimeError("pdftoppm not found on PATH (install Poppler, e.g. brew install poppler)")
    # -singlefile: single page -> exactly outprefix.png
    prefix = out_png.with_suffix("")
    cmd = [
        pdftoppm,
        "-png",
        "-f",
        str(page_1based),
        "-l",
        str(page_1based),
        "-singlefile",
        str(pdf_path),
        str(prefix),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"pdftoppm failed (exit {proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}"
        )
    expected = Path(str(prefix) + ".png")
    if not expected.is_file():
        # Some versions may use different naming; try glob
        matches = sorted(glob.glob(str(prefix) + "*.png"))
        if len(matches) == 1:
            Path(matches[0]).rename(expected)
        elif not matches:
            raise RuntimeError(f"pdftoppm produced no PNG for page {page_1based}")
        else:
            raise RuntimeError(f"pdftoppm produced unexpected files: {matches}")
    if expected != out_png:
        expected.rename(out_png)


def render_page_pymupdf(pdf_path: Path, page_1based: int, out_png: Path, dpi: int) -> None:
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF (fitz) is not importable. Install with: pip install pymupdf"
        ) from exc
    doc = fitz.open(str(pdf_path))
    try:
        idx = page_1based - 1
        if idx < 0 or idx >= len(doc):
            raise ValueError(f"page {page_1based} out of range (1..{len(doc)})")
        page = doc[idx]
        pix = page.get_pixmap(dpi=dpi)
        pix.save(str(out_png))
    finally:
        doc.close()


def render_page(pdf_path: Path, page_1based: int, out_png: Path, dpi: int) -> None:
    errors: list[str] = []
    if find_executable("pdftoppm"):
        try:
            render_page_pdftoppm(pdf_path, page_1based, out_png)
            return
        except Exception as exc:  # noqa: BLE001 - aggregate fallbacks
            errors.append(f"pdftoppm: {exc}")
    try:
        render_page_pymupdf(pdf_path, page_1based, out_png, dpi=dpi)
        return
    except Exception as exc:  # noqa: BLE001
        errors.append(f"pymupdf: {exc}")
    detail = "; ".join(errors) if errors else "no renderer available"
    raise RuntimeError(
        "Could not render PDF page to image. "
        "Install Poppler (pdftoppm on PATH) or PyMuPDF (pip install pymupdf). "
        f"Details: {detail}"
    )


def run_tesseract(png_path: Path, lang: str) -> str:
    tess = find_executable("tesseract")
    if not tess:
        raise RuntimeError(
            "tesseract not found on PATH. Install: brew install tesseract tesseract-lang (macOS) "
            "or use your OS package manager."
        )
    cmd = [tess, str(png_path), "stdout", "-l", lang]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"tesseract failed (exit {proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}"
        )
    return proc.stdout or ""


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def ocr_pdf_pages(pdf_path: Path, pages: list[int], lang: str, dpi: int) -> str:
    total = pdf_page_count(pdf_path)
    chunks: list[str] = []
    for page_no in pages:
        if page_no > total:
            raise ValueError(f"page {page_no} out of range (PDF has {total} page(s))")
        with tempfile.TemporaryDirectory(prefix="pdf_ocr_") as tmp:
            png = Path(tmp) / "page.png"
            render_page(pdf_path, page_no, png, dpi=dpi)
            raw = run_tesseract(png, lang=lang)
            text = normalize_text(raw)
            if text:
                chunks.append(f"[PDF OCR page {page_no}]\n{text}")
            else:
                chunks.append(f"[PDF OCR page {page_no}]\n(empty OCR result)")
    return "\n\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="OCR selected pages of a PDF using tesseract (and pdftoppm or PyMuPDF)."
    )
    parser.add_argument("source", help="Path to a .pdf file")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--page", type=int, metavar="N", help="Single 1-based page number")
    g.add_argument(
        "--pages",
        metavar="SPEC",
        help="Comma-separated pages and ranges, e.g. 1,3-5,7",
    )
    parser.add_argument(
        "--lang",
        default="eng+kor",
        help="Tesseract language(s), default: eng+kor",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI when rendering with PyMuPDF (ignored for pdftoppm)",
    )
    args = parser.parse_args()

    pdf_path = Path(args.source).expanduser().resolve()
    if not pdf_path.is_file():
        print(f"error: file not found: {pdf_path}", file=sys.stderr)
        return 2
    if pdf_path.suffix.lower() != ".pdf":
        print("error: only .pdf is supported", file=sys.stderr)
        return 2

    try:
        if args.page is not None:
            if args.page < 1:
                print("error: --page must be >= 1", file=sys.stderr)
                return 2
            page_list = [args.page]
        else:
            page_list = parse_page_spec(args.pages or "")
            if not page_list:
                print("error: no pages parsed from --pages", file=sys.stderr)
                return 2
        text = ocr_pdf_pages(pdf_path, page_list, lang=args.lang, dpi=args.dpi)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    sys.stdout.write(text)
    if text and not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
