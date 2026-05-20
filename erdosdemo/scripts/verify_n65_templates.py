#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import Counter
from fractions import Fraction
from pathlib import Path


EXPECTED_TOTAL = 137
EXPECTED_BACKBONES = {"2+31": 68, "19+37": 69}
EXPECTED_TEMPLATES = {
    "2+31 + {8,24}": 63,
    "2+31 + {12,20}": 5,
    "19+37 + {22}": 58,
    "19+37 + {21,23}": 11,
}


def default_csv_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "anomalies_N65_candidates.csv"


def parse_denominators(text: str) -> set[int]:
    separator = ";" if ";" in text else ","
    return {int(value.strip()) for value in text.split(separator) if value.strip()}


def reciprocal_sum(denominators: set[int]) -> Fraction:
    return sum((Fraction(1, denominator) for denominator in denominators), Fraction(0, 1))


def classify(row: dict[str, str], denominators: set[int]) -> str:
    backbone = row["escaped_backbone"]
    if backbone == "2+31":
        if {8, 24} <= denominators:
            return "2+31 + {8,24}"
        if {12, 20} <= denominators:
            return "2+31 + {12,20}"
    if backbone == "19+37":
        if 22 in denominators:
            return "19+37 + {22}"
        if {21, 23} <= denominators:
            return "19+37 + {21,23}"
    return "unclassified"


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the finite N=65 anomaly template split.")
    parser.add_argument("csv_path", nargs="?", type=Path, default=default_csv_path())
    parser.add_argument("--low", default="99/100")
    parser.add_argument("--high", default="101/100")
    args = parser.parse_args()

    low = Fraction(args.low)
    high = Fraction(args.high)
    rows: list[dict[str, str]] = []
    errors: list[str] = []
    backbone_counts: Counter[str] = Counter()
    template_counts: Counter[str] = Counter()
    unclassified: list[str] = []

    with args.csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):
            rows.append(row)
            backbone = row.get("escaped_backbone", "")
            denominators = parse_denominators(row.get("denominators", ""))
            backbone_counts[backbone] += 1

            total = reciprocal_sum(denominators)
            if not low <= total <= high:
                errors.append(f"row {row_number}: reciprocal sum {total} outside [{low}, {high}]")

            if backbone == "2+31" and not {15, 17} <= denominators:
                errors.append(f"row {row_number}: 2+31 row misses forced core {{15,17}}")
            if backbone == "19+37" and not {18, 20} <= denominators:
                errors.append(f"row {row_number}: 19+37 row misses forced core {{18,20}}")

            label = classify(row, denominators)
            if label == "unclassified":
                unclassified.append(row.get("candidate_id", f"row {row_number}"))
            else:
                template_counts[label] += 1

    if len(rows) != EXPECTED_TOTAL:
        errors.append(f"expected {EXPECTED_TOTAL} rows, found {len(rows)}")
    for backbone, expected in EXPECTED_BACKBONES.items():
        if backbone_counts[backbone] != expected:
            errors.append(f"expected {expected} rows for {backbone}, found {backbone_counts[backbone]}")
    for label, expected in EXPECTED_TEMPLATES.items():
        if template_counts[label] != expected:
            errors.append(f"expected {expected} rows for {label}, found {template_counts[label]}")
    if unclassified:
        errors.append(f"unclassified rows: {len(unclassified)}")

    print(f"csv: {args.csv_path}")
    print(f"rows: {len(rows)}")
    print("backbone counts:")
    for backbone in sorted(EXPECTED_BACKBONES):
        print(f"  {backbone}: {backbone_counts[backbone]}")
    print("template counts:")
    for label in EXPECTED_TEMPLATES:
        print(f"  {label}: {template_counts[label]}")
    print(f"unclassified rows: {len(unclassified)}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"  {error}")
        raise SystemExit(1)

    print("PASS")


if __name__ == "__main__":
    main()
