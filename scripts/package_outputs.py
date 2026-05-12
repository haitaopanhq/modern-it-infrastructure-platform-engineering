#!/usr/bin/env python3
"""Package generated document outputs into release archives."""

from __future__ import annotations

import argparse
import tarfile
from pathlib import Path


ARCHIVES = {
    "all": ("modern-it-infrastructure-platform-engineering.tar.gz", None),
    "pdf": ("modern-it-infrastructure-platform-engineering-pdf.tar.gz", ".pdf"),
    "docx": ("modern-it-infrastructure-platform-engineering-docx.tar.gz", ".docx"),
    "html": ("modern-it-infrastructure-platform-engineering-html.tar.gz", ".html"),
}


def iter_files(output_dir: Path, suffix: str | None) -> list[Path]:
    files = [path for path in output_dir.rglob("*") if path.is_file()]
    if suffix is not None:
        files = [path for path in files if path.suffix == suffix]
    return sorted(files)


def write_archive(output_dir: Path, dist_dir: Path, archive_name: str, suffix: str | None) -> Path:
    archive_path = dist_dir / archive_name
    files = iter_files(output_dir, suffix)
    if not files:
        label = suffix or "any generated output"
        raise SystemExit(f"No files found for {label}")

    with tarfile.open(archive_path, "w:gz") as archive:
        for path in files:
            archive.add(path, arcname=path.relative_to(output_dir))

    return archive_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--dist-dir", default="dist")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    dist_dir = Path(args.dist_dir)
    if not output_dir.is_dir():
        raise SystemExit(f"Output directory does not exist: {output_dir}")

    dist_dir.mkdir(parents=True, exist_ok=True)
    for archive_name, suffix in ARCHIVES.values():
        archive_path = write_archive(output_dir, dist_dir, archive_name, suffix)
        print(f"Packaged {archive_path}")


if __name__ == "__main__":
    main()
