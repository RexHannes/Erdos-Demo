#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from verify_woett_chain import read_chain, verify_chain  # noqa: E402


def module_root() -> Path:
    return Path(__file__).resolve().parents[1]


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def write_intervals(path: Path, chain: list[int], N: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["p", "coverage_start", "coverage_end", "clipped_start", "clipped_end", "covers_any_up_to_N"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for p in chain:
            start = p + 1
            end = 2 * p - 3
            clipped_start = max(1, start)
            clipped_end = min(N, end)
            writer.writerow(
                {
                    "p": p,
                    "coverage_start": start,
                    "coverage_end": end,
                    "clipped_start": clipped_start,
                    "clipped_end": clipped_end,
                    "covers_any_up_to_N": clipped_start <= clipped_end,
                }
            )


def covered_values(chain: list[int], N: int) -> set[int]:
    covered: set[int] = set()
    for p in chain:
        start = max(1, p + 1)
        end = min(N, 2 * p - 3)
        if start <= end:
            covered.update(range(start, end + 1))
    return covered


def write_holes(path: Path, holes: list[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["M"])
        writer.writeheader()
        for M in holes:
            writer.writerow({"M": M})


def main() -> None:
    root = module_root()
    parser = argparse.ArgumentParser(description="Scan uncovered M values for a Woett-good prime chain.")
    parser.add_argument("--N", type=int, required=True)
    parser.add_argument("--chain", type=Path, default=root / "data" / "woett_chain.txt")
    parser.add_argument("--results-dir", type=Path, default=root / "results")
    parser.add_argument("--allow-invalid-chain", action="store_true")
    args = parser.parse_args()

    if args.N < 1:
        raise SystemExit("--N must be positive")

    chain = read_chain(args.chain)
    _, errors = verify_chain(chain)
    if errors and not args.allow_invalid_chain:
        print("Chain verification failed; refusing to scan holes.")
        for error in errors:
            print(f"  {error}")
        raise SystemExit(1)

    intervals_path = args.results_dir / "woett_coverage_intervals.csv"
    holes_path = args.results_dir / f"woett_holes_M_le_{args.N}.csv"
    write_intervals(intervals_path, chain, args.N)

    covered = covered_values(chain, args.N)
    holes = [M for M in range(1, args.N + 1) if M not in covered]
    write_holes(holes_path, holes)

    print(f"N: {args.N}")
    print(f"chain: {display_path(args.chain)}")
    print(f"coverage_intervals: {display_path(intervals_path)}")
    print(f"holes_csv: {display_path(holes_path)}")
    print(f"holes: {len(holes)}")
    if holes:
        preview = ",".join(str(M) for M in holes[:20])
        suffix = "" if len(holes) <= 20 else ",..."
        print(f"holes_preview: {preview}{suffix}")
    print("PASS")


if __name__ == "__main__":
    main()
