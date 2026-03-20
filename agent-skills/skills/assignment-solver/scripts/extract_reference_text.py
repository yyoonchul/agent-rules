#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
VENDOR_DIR = SKILL_DIR / "vendor"

if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

from olefile import OleFileIO  # type: ignore
from pypdf import PdfReader  # type: ignore


DRAWINGML_NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
PPT_TEXT_CHARS_ATOM = 0x0FA0
PPT_TEXT_BYTES_ATOM = 0x0FA8


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract plain text from PDF, PPTX, or PPT using bundled skill modules."
    )
    parser.add_argument("source", help="Path to a .pdf, .pptx, or .ppt file")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.is_file():
        print(f"error: file not found: {source}", file=sys.stderr)
        return 2

    try:
        text = extract_text(source)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    sys.stdout.write(text)
    if text and not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


def extract_text(source: Path) -> str:
    suffix = source.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf_text(source)
    if suffix == ".pptx":
        return extract_pptx_text(source)
    if suffix == ".ppt":
        return extract_ppt_text(source)
    raise ValueError(f"unsupported file type: {source.suffix}")


def extract_pdf_text(source: Path) -> str:
    reader = PdfReader(str(source))
    chunks: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = normalize_text(page.extract_text() or "")
        if text:
            chunks.append(f"[PDF page {index}]\n{text}")
    if not chunks:
        raise ValueError("no extractable text found in PDF")
    return "\n\n".join(chunks)


def extract_pptx_text(source: Path) -> str:
    chunks: list[str] = []
    with zipfile.ZipFile(source) as archive:
        slide_paths = sorted(
            (name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
            key=slide_sort_key,
        )
        if not slide_paths:
            raise ValueError("no slide XML found in PPTX")

        for slide_number, slide_path in enumerate(slide_paths, start=1):
            slide_xml = archive.read(slide_path)
            slide_text = extract_drawingml_text(slide_xml)
            notes_path = f"ppt/notesSlides/notesSlide{slide_number}.xml"
            notes_text = ""
            if notes_path in archive.namelist():
                notes_text = extract_drawingml_text(archive.read(notes_path))

            parts: list[str] = []
            if slide_text:
                parts.append(slide_text)
            if notes_text:
                parts.append(f"[Notes]\n{notes_text}")
            if parts:
                chunks.append(f"[PPTX slide {slide_number}]\n" + "\n\n".join(parts))

    if not chunks:
        raise ValueError("no extractable text found in PPTX")
    return "\n\n".join(chunks)


def extract_ppt_text(source: Path) -> str:
    with OleFileIO(str(source)) as ole:
        if not ole.exists("PowerPoint Document"):
            raise ValueError("missing PowerPoint Document stream in PPT")
        payload = ole.openstream("PowerPoint Document").read()

    lines: list[str] = []
    for record_type, record_data in iter_ppt_records(payload):
        if record_type == PPT_TEXT_CHARS_ATOM:
            text = record_data.decode("utf-16le", errors="ignore")
        elif record_type == PPT_TEXT_BYTES_ATOM:
            text = record_data.decode("latin1", errors="ignore")
        else:
            continue
        for line in split_text_chunks(text):
            lines.append(line)

    lines = dedupe(lines)
    if lines:
        return "[PPT extracted text]\n" + "\n".join(lines)

    fallback_lines = extract_probable_strings(payload)
    if fallback_lines:
        return "[PPT extracted text - fallback]\n" + "\n".join(fallback_lines)

    raise ValueError("no extractable text found in PPT")


def slide_sort_key(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def extract_drawingml_text(xml_bytes: bytes) -> str:
    root = ET.fromstring(xml_bytes)
    text_runs = [normalize_text(node.text or "") for node in root.findall(".//a:t", DRAWINGML_NS)]
    text_runs = [text for text in text_runs if text]
    return "\n".join(text_runs)


def iter_ppt_records(blob: bytes) -> Iterable[tuple[int, bytes]]:
    def walk(segment: bytes) -> Iterable[tuple[int, bytes]]:
        cursor = 0
        limit = len(segment)
        while cursor + 8 <= limit:
            header = int.from_bytes(segment[cursor : cursor + 2], "little")
            record_version = header & 0x000F
            record_type = int.from_bytes(segment[cursor + 2 : cursor + 4], "little")
            record_length = int.from_bytes(segment[cursor + 4 : cursor + 8], "little")
            data_start = cursor + 8
            data_end = data_start + record_length
            if data_end > limit:
                break
            data = segment[data_start:data_end]
            yield record_type, data
            if record_version == 0x000F:
                yield from walk(data)
            cursor = data_end

    yield from walk(blob)


def split_text_chunks(text: str) -> list[str]:
    text = text.replace("\r", "\n").replace("\x0b", "\n").replace("\x00", "")
    parts = [normalize_text(part) for part in text.split("\n")]
    return [part for part in parts if looks_like_text(part)]


def extract_probable_strings(blob: bytes) -> list[str]:
    candidates: list[str] = []

    for offset in (0, 1):
        even_length = (len(blob) - offset) // 2 * 2
        if even_length <= 0:
            continue
        decoded = blob[offset : offset + even_length].decode("utf-16le", errors="ignore")
        for part in re.split(r"[\x00-\x1f]+", decoded):
            part = normalize_text(part)
            if looks_like_text(part):
                candidates.append(part)

    for match in re.finditer(rb"[\x20-\x7e]{4,}", blob):
        part = normalize_text(match.group().decode("latin1", errors="ignore"))
        if looks_like_text(part):
            candidates.append(part)

    return dedupe(candidates)


def looks_like_text(value: str) -> bool:
    if len(value) < 3:
        return False
    if not re.search(r"[0-9A-Za-z\u00C0-\u024F\u0400-\u04FF\u3040-\u30FF\u3400-\u9FFF\uAC00-\uD7AF]", value):
        return False
    alpha_num = sum(ch.isalnum() for ch in value)
    return alpha_num >= max(2, len(value) // 6)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def dedupe(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


if __name__ == "__main__":
    raise SystemExit(main())
