#!/usr/bin/env python3
"""Collate yearly POST data files into POST-data-TOTAL.txt.

Behavior:
- Reads data/POST-data-*.txt (excluding POST-data-TOTAL.txt)
- Maps year-specific row layouts to the union schema
- Deduplicates by exact full-row text after normalization
- Writes tab-separated output with a single header row
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

BASE_FIELDS = [
    "testID",
    "testCounter",
    "testPARAMS",
    "T0_IDLE",
    "T1_WARN",
    "T2_SHOWTEST",
    "T3_DECAY",
    "T4_COUNTDOWN",
    "requested_sequence",
    "recorded_sequence",
    "status",
    "elapsed_frames",
    "remaining_levels",
    "window_size",
]

EXTRA_2024 = ["age", "hours_awake", "substance_use"]
EXTRA_2025 = ["colorblind"]
EXTRA_2026 = ["instructions", "experience"]

CANONICAL_SCHEMA = BASE_FIELDS + EXTRA_2024 + EXTRA_2025 + EXTRA_2026 + ["dtstamp"]


@dataclass
class Stats:
    files_used: int = 0
    rows_read: int = 0
    rows_written: int = 0
    rows_skipped: int = 0
    duplicates_removed: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collate yearly POST-data files into a normalized TOTAL file."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory containing POST-data-*.txt files (default: script directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file path (default: <data-dir>/POST-data-TOTAL.txt).",
    )
    return parser.parse_args()


def discover_inputs(data_dir: Path, output_path: Path) -> list[Path]:
    candidates = sorted(data_dir.glob("POST-data-*.txt"))
    result = [p for p in candidates if p.resolve() != output_path.resolve()]
    return result


def map_row_to_schema(fields: list[str]) -> list[str] | None:
    """Map known yearly row layouts (15/18/19/21 columns) to canonical schema."""
    # Ignore accidental header rows in source files.
    if fields and fields[0] == "testID":
        return None

    size = len(fields)

    if size not in (15, 18, 19, 21):
        return None

    base = fields[:14]
    dtstamp = fields[-1]

    age = ""
    hours_awake = ""
    substance_use = ""
    colorblind = ""
    instructions = ""
    experience = ""

    if size >= 18:
        age, hours_awake, substance_use = fields[14:17]
    if size >= 19:
        colorblind = fields[17]
    if size >= 21:
        instructions, experience = fields[18:20]

    return (
        base
        + [age, hours_awake, substance_use, colorblind, instructions, experience, dtstamp]
    )


def iter_rows(input_files: Iterable[Path], stats: Stats) -> Iterable[list[str]]:
    for input_file in input_files:
        stats.files_used += 1
        with input_file.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle, delimiter="\t")
            for row in reader:
                if not row:
                    continue

                stats.rows_read += 1
                mapped = map_row_to_schema(row)
                if mapped is None:
                    stats.rows_skipped += 1
                    continue

                yield mapped


def write_output(output_path: Path, rows: Iterable[list[str]], stats: Stats) -> None:
    seen: set[str] = set()

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(CANONICAL_SCHEMA)

        for row in rows:
            row_key = "\t".join(row)
            if row_key in seen:
                stats.duplicates_removed += 1
                continue

            seen.add(row_key)
            writer.writerow(row)
            stats.rows_written += 1


def main() -> int:
    args = parse_args()
    data_dir = args.data_dir.resolve()
    output_path = (args.output or (data_dir / "POST-data-TOTAL.txt")).resolve()

    stats = Stats()
    input_files = discover_inputs(data_dir=data_dir, output_path=output_path)

    if not input_files:
        print("No input files found matching POST-data-*.txt")
        return 1

    rows = iter_rows(input_files=input_files, stats=stats)
    write_output(output_path=output_path, rows=rows, stats=stats)

    print(f"Output: {output_path}")
    print("Inputs:")
    for path in input_files:
        print(f"- {path}")
    print("Stats:")
    print(f"- rows_read={stats.rows_read}")
    print(f"- rows_written={stats.rows_written}")
    print(f"- duplicates_removed={stats.duplicates_removed}")
    print(f"- rows_skipped={stats.rows_skipped}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
