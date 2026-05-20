#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BlockCheck:
    label: str
    denominators: tuple[int, ...]
    prime: int
    expected_max_valuation: int
    expected_top_denominators: tuple[int, ...]
    expected_residue_sum: int


CHECKS = (
    BlockCheck("{8,24} top-2 cancellation", (8, 24), 2, 3, (8, 24), 0),
    BlockCheck("{12,20} top-2 cancellation", (12, 20), 2, 2, (12, 20), 0),
    BlockCheck("{18,20,22} mod-19 residue", (18, 20, 22), 19, 0, (18, 20, 22), 13),
    BlockCheck("{18,20,22} mod-37 residue", (18, 20, 22), 37, 0, (18, 20, 22), 6),
    BlockCheck("{18,20,21,23} mod-19 residue", (18, 20, 21, 23), 19, 0, (18, 20, 21, 23), 15),
    BlockCheck("{18,20,21,23} mod-37 residue", (18, 20, 21, 23), 37, 0, (18, 20, 21, 23), 33),
)


def valuation(value: int, prime: int) -> int:
    count = 0
    while value % prime == 0:
        value //= prime
        count += 1
    return count


def reduced_unit(value: int, prime: int, exponent: int) -> int:
    for _ in range(exponent):
        value //= prime
    return value % prime


def residue_snapshot(denominators: tuple[int, ...], prime: int) -> tuple[int, tuple[int, ...], int]:
    max_valuation = max(valuation(denominator, prime) for denominator in denominators)
    top_denominators = tuple(
        denominator for denominator in denominators if valuation(denominator, prime) == max_valuation
    )
    residue_sum = sum(
        pow(reduced_unit(denominator, prime, max_valuation), -1, prime)
        for denominator in top_denominators
    ) % prime
    return max_valuation, top_denominators, residue_sum


def main() -> None:
    errors: list[str] = []
    for check in CHECKS:
        actual = residue_snapshot(check.denominators, check.prime)
        expected = (
            check.expected_max_valuation,
            check.expected_top_denominators,
            check.expected_residue_sum,
        )
        print(
            f"{check.label}: max_v={actual[0]} top={actual[1]} residue_mod_{check.prime}={actual[2]}"
        )
        if actual != expected:
            errors.append(f"{check.label}: expected {expected}, found {actual}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"  {error}")
        raise SystemExit(1)

    print("PASS")


if __name__ == "__main__":
    main()
