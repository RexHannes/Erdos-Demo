#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


PRIMES_UP_TO_70 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67)
BACKBONES = ((2, 31), (19, 37))
EXPECTED_ROWS = 137
EXPECTED_BACKBONE_COUNTS = {"2+31": 68, "19+37": 69}


@dataclass(frozen=True)
class Dataset:
    label: str
    path: Path
    rows: tuple[tuple[int, ...], ...]
    escape_counts: Counter[str]
    max_denominator: int

    @property
    def row_set(self) -> set[tuple[int, ...]]:
        return set(self.rows)


def repo_demo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_denominators(text: str) -> tuple[int, ...]:
    separator = ";" if ";" in text else ","
    values = tuple(sorted(int(value.strip()) for value in text.split(separator) if value.strip()))
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate denominators in {text!r}")
    return values


def valuation(value: int, prime: int) -> int:
    count = 0
    while value % prime == 0:
        value //= prime
        count += 1
    return count


def top_layer_residue(denominators: tuple[int, ...], prime: int) -> tuple[int, int]:
    max_v = max(valuation(denominator, prime) for denominator in denominators)
    residue = 0
    for denominator in denominators:
        if valuation(denominator, prime) != max_v:
            continue
        reduced = denominator
        for _ in range(max_v):
            reduced //= prime
        residue = (residue + pow(reduced % prime, -1, prime)) % prime
    return max_v, residue


def kills_prime(denominators: tuple[int, ...], prime: int) -> bool:
    max_v, residue = top_layer_residue(denominators, prime)
    # If p divides no denominator, compare the reciprocal sum to 1 modulo p.
    adjusted = residue - 1 if max_v == 0 else residue
    return adjusted % prime != 0


def escaped_backbones(denominators: tuple[int, ...]) -> tuple[str, ...]:
    escaped: list[str] = []
    for left, right in BACKBONES:
        if not kills_prime(denominators, left) and not kills_prime(denominators, right):
            escaped.append(f"{left}+{right}")
    return tuple(escaped)


def reciprocal_sum(denominators: tuple[int, ...]) -> Fraction:
    return sum((Fraction(1, denominator) for denominator in denominators), Fraction(0, 1))


def has_gap_at_most_two(denominators: tuple[int, ...]) -> bool:
    return all(right - left <= 2 for left, right in zip(denominators, denominators[1:]))


def load_dataset(label: str, path: Path, low: Fraction, high: Fraction, errors: list[str]) -> Dataset:
    rows: list[tuple[int, ...]] = []
    escape_counts: Counter[str] = Counter()
    max_denominator = 0

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if "denominators" not in (reader.fieldnames or ()):
            errors.append(f"{label}: missing denominators column")
            return Dataset(label, path, tuple(), Counter(), 0)

        for row_number, row in enumerate(reader, start=2):
            try:
                denominators = parse_denominators(row["denominators"])
            except ValueError as exc:
                errors.append(f"{label} row {row_number}: {exc}")
                continue

            rows.append(denominators)
            max_denominator = max(max_denominator, max(denominators))

            total = reciprocal_sum(denominators)
            if not low <= total <= high:
                errors.append(f"{label} row {row_number}: reciprocal sum {total} outside [{low}, {high}]")
            if not has_gap_at_most_two(denominators):
                errors.append(f"{label} row {row_number}: denominator gap exceeds 2")

            escaped = escaped_backbones(denominators)
            if not escaped:
                errors.append(f"{label} row {row_number}: escapes neither tracked backbone")
            for backbone in escaped:
                escape_counts[backbone] += 1
                if backbone == "2+31" and not {15, 17} <= set(denominators):
                    errors.append(f"{label} row {row_number}: computed 2+31 escape misses forced core {{15,17}}")
                if backbone == "19+37" and not {18, 20} <= set(denominators):
                    errors.append(f"{label} row {row_number}: computed 19+37 escape misses forced core {{18,20}}")

    return Dataset(label, path, tuple(rows), escape_counts, max_denominator)


def check_main_dataset(dataset: Dataset, errors: list[str]) -> None:
    if len(dataset.rows) != EXPECTED_ROWS:
        errors.append(f"{dataset.label}: expected {EXPECTED_ROWS} rows, found {len(dataset.rows)}")
    if len(dataset.row_set) != len(dataset.rows):
        errors.append(f"{dataset.label}: duplicate normalized denominator rows found")
    if dataset.max_denominator != 36:
        errors.append(f"{dataset.label}: expected max denominator 36, found {dataset.max_denominator}")
    for label, expected in EXPECTED_BACKBONE_COUNTS.items():
        if dataset.escape_counts[label] != expected:
            errors.append(
                f"{dataset.label}: expected {expected} computed {label} escapes, "
                f"found {dataset.escape_counts[label]}"
            )


def compare_sets(left: Dataset, right: Dataset) -> tuple[int, int]:
    return len(left.row_set - right.row_set), len(right.row_set - left.row_set)


def main() -> None:
    root = repo_demo_root()
    parser = argparse.ArgumentParser(
        description="Independent N65/N70 audit using only the denominators column."
    )
    parser.add_argument("--n65", type=Path, default=root / "data" / "anomalies_N65_candidates.csv")
    parser.add_argument("--n70", type=Path, default=root / "data" / "anomalies_N70_candidates.csv")
    parser.add_argument("--n35", type=Path, default=root / "data" / "sentinel" / "anomalies_N35_candidates.csv")
    parser.add_argument("--n36", type=Path, default=root / "data" / "sentinel" / "anomalies_N36_candidates.csv")
    parser.add_argument("--low", default="99/100")
    parser.add_argument("--high", default="101/100")
    args = parser.parse_args()

    low = Fraction(args.low)
    high = Fraction(args.high)
    errors: list[str] = []

    n65 = load_dataset("N65", args.n65, low, high, errors)
    n70 = load_dataset("N70", args.n70, low, high, errors)
    check_main_dataset(n65, errors)
    check_main_dataset(n70, errors)
    n65_missing, n70_missing = compare_sets(n65, n70)
    if n65_missing or n70_missing:
        errors.append(f"N65/N70 normalized row sets differ: {n65_missing} vs {n70_missing}")

    print(f"N65 rows: {len(n65.rows)}")
    print(f"N70 rows: {len(n70.rows)}")
    print(f"N65 not in N70: {n65_missing}")
    print(f"N70 not in N65: {n70_missing}")
    print(f"max denominator N65: {n65.max_denominator}")
    print(f"max denominator N70: {n70.max_denominator}")
    print("computed backbone counts:")
    for label in sorted(EXPECTED_BACKBONE_COUNTS):
        print(f"  N65 {label}: {n65.escape_counts[label]}")
        print(f"  N70 {label}: {n70.escape_counts[label]}")

    if args.n35.exists() and args.n36.exists():
        n35 = load_dataset("N35 sentinel", args.n35, low, high, errors)
        n36 = load_dataset("N36 sentinel", args.n36, low, high, errors)
        n36_not_n70, n70_not_n36 = compare_sets(n36, n70)
        n36_vs_n70_difference = n36_not_n70 + n70_not_n36
        if len(n35.rows) >= len(n36.rows):
            errors.append(f"N35 sentinel should have fewer rows than N36, found {len(n35.rows)} >= {len(n36.rows)}")
        if len(n36.rows) != EXPECTED_ROWS:
            errors.append(f"N36 sentinel expected {EXPECTED_ROWS} rows, found {len(n36.rows)}")
        if n36_vs_n70_difference != 0:
            errors.append(f"N36/N70 sentinel row sets differ by {n36_vs_n70_difference} rows")

        print("sentinel:")
        print(f"  N35 rows: {len(n35.rows)}")
        print(f"  N36 rows: {len(n36.rows)}")
        print(f"  N70 rows: {len(n70.rows)}")
        print(f"  N36 vs N70 difference count: {n36_vs_n70_difference}")
    else:
        print("sentinel: skipped; N35/N36 files not found")

    print(f"errors: {len(errors)}")
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
