#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


try:
    from sympy import isprime as _sympy_isprime  # type: ignore
except Exception:  # pragma: no cover - sympy is optional.
    _sympy_isprime = None


# Deterministic Miller-Rabin bases for all n < 2^64.
MR_64_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def module_root() -> Path:
    return Path(__file__).resolve().parents[1]


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def read_chain(path: Path) -> list[int]:
    values: list[int] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        try:
            values.append(int(line))
        except ValueError as exc:
            raise ValueError(f"{path}:{line_number}: expected an integer, found {raw!r}") from exc
    return values


def _miller_rabin_64(n: int) -> bool:
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for base in MR_64_BASES:
        if base >= n:
            continue
        x = pow(base, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def is_prime(n: int) -> bool:
    if _sympy_isprime is not None:
        return bool(_sympy_isprime(n))
    if n < 2**64:
        return _miller_rabin_64(n)
    raise ValueError("Install sympy for exact primality testing on integers >= 2^64.")


def good_prime_side(p: int) -> str:
    minus = is_prime((p - 1) // 2) if (p - 1) % 2 == 0 else False
    plus = is_prime((p + 1) // 2) if (p + 1) % 2 == 0 else False
    if minus and plus:
        return "both"
    if minus:
        return "minus"
    if plus:
        return "plus"
    return "none"


def verify_chain(chain: list[int]) -> tuple[list[dict[str, object]], list[str]]:
    rows: list[dict[str, object]] = []
    errors: list[str] = []
    seen: set[int] = set()

    for index, p in enumerate(chain):
        next_p = chain[index + 1] if index + 1 < len(chain) else None
        p_prime = is_prime(p)
        side = good_prime_side(p) if p_prime else "none"
        good = p_prime and side != "none"
        interval_start = p + 1
        interval_end = 2 * p - 3
        next_ok = next_p is None or next_p <= interval_end

        if p in seen:
            errors.append(f"duplicate p={p}")
        seen.add(p)
        if index and p <= chain[index - 1]:
            errors.append(f"chain is not strictly increasing at p={p}")
        if not p_prime:
            errors.append(f"p={p} is not prime")
        if p_prime and not good:
            errors.append(f"p={p} is prime but not Woett-good")
        if not next_ok:
            errors.append(f"chain gap: next p={next_p} exceeds 2*p-3={interval_end} for p={p}")

        rows.append(
            {
                "index": index,
                "p": p,
                "is_prime": p_prime,
                "half_minus": (p - 1) // 2,
                "half_minus_prime": is_prime((p - 1) // 2) if (p - 1) % 2 == 0 else False,
                "half_plus": (p + 1) // 2,
                "half_plus_prime": is_prime((p + 1) // 2) if (p + 1) % 2 == 0 else False,
                "good_side": side,
                "is_woett_good": good,
                "coverage_start": interval_start,
                "coverage_end": interval_end,
                "next_p": "" if next_p is None else next_p,
                "chain_condition_next_ok": next_ok,
            }
        )
    return rows, errors


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "index",
        "p",
        "is_prime",
        "half_minus",
        "half_minus_prime",
        "half_plus",
        "half_plus_prime",
        "good_side",
        "is_woett_good",
        "coverage_start",
        "coverage_end",
        "next_p",
        "chain_condition_next_ok",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    root = module_root()
    parser = argparse.ArgumentParser(description="Verify a Woett-good prime chain.")
    parser.add_argument("--chain", type=Path, default=root / "data" / "woett_chain.txt")
    parser.add_argument("--results-dir", type=Path, default=root / "results")
    args = parser.parse_args()

    chain = read_chain(args.chain)
    rows, errors = verify_chain(chain)

    csv_path = args.results_dir / "woett_chain_verified.csv"
    summary_path = args.results_dir / "woett_summary.json"
    write_csv(csv_path, rows)

    covered_start = rows[0]["coverage_start"] if rows else None
    covered_end = max((int(row["coverage_end"]) for row in rows), default=None)
    summary = {
        "chain_path": display_path(args.chain),
        "prime_count": len(chain),
        "first_p": chain[0] if chain else None,
        "last_p": chain[-1] if chain else None,
        "covered_start": covered_start,
        "covered_end": covered_end,
        "valid": not errors,
        "errors": errors,
    }
    args.results_dir.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"chain: {display_path(args.chain)}")
    print(f"primes: {len(chain)}")
    print(f"verified_csv: {display_path(csv_path)}")
    print(f"summary_json: {display_path(summary_path)}")
    print(f"errors: {len(errors)}")
    if errors:
        print("FAIL")
        for error in errors:
            print(f"  {error}")
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
