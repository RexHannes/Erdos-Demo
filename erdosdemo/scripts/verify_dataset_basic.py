#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from fractions import Fraction
from pathlib import Path


def default_csv_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "anomalies_N65_candidates.csv"


def parse_denominators(text: str) -> list[int]:
    separator = ";" if ";" in text else ","
    return [int(value.strip()) for value in text.split(separator) if value.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Basic independent checks for the N=65 anomaly CSV.")
    parser.add_argument("csv_path", nargs="?", type=Path, default=default_csv_path())
    parser.add_argument("--low", default="99/100")
    parser.add_argument("--high", default="101/100")
    parser.add_argument("--max-denominator", type=int, default=65)
    args = parser.parse_args()

    low = Fraction(args.low)
    high = Fraction(args.high)
    rows = 0
    errors: list[str] = []
    max_distribution: Counter[int] = Counter()

    with args.csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):
            rows += 1
            denominators = parse_denominators(row.get("denominators", ""))
            if not denominators:
                errors.append(f"row {row_number}: empty denominator set")
                continue

            row_max = max(denominators)
            max_distribution[row_max] += 1
            if row_max > args.max_denominator:
                errors.append(f"row {row_number}: max denominator {row_max} > {args.max_denominator}")

            total = sum((Fraction(1, denominator) for denominator in denominators), Fraction(0, 1))
            if not low <= total <= high:
                errors.append(f"row {row_number}: reciprocal sum {total} outside [{low}, {high}]")

    print(f"csv: {args.csv_path}")
    print(f"sha256: {sha256(args.csv_path)}")
    print(f"rows: {rows}")
    print("max denominator distribution:")
    for denominator, count in sorted(max_distribution.items()):
        print(f"  {denominator}: {count}")

    if errors:
        print("FAIL")
        for error in errors[:100]:
            print(f"  {error}")
        if len(errors) > 100:
            print(f"  ... {len(errors) - 100} more errors")
        raise SystemExit(1)

    print("PASS")


if __name__ == "__main__":
    main()
