#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TopLayerResidue:
    prime: int
    max_valuation: int
    top_denominators: tuple[int, ...]
    residue_sum_mod_q: int


def valuation(value: int, q: int) -> int:
    if q < 2:
        raise ValueError("q must be at least 2")
    if value <= 0:
        raise ValueError("denominators must be positive")
    count = 0
    while value % q == 0:
        value //= q
        count += 1
    return count


def top_layer_residue_sum(S: Iterable[int], q: int) -> TopLayerResidue:
    denominators = tuple(sorted(int(value) for value in S))
    if not denominators:
        raise ValueError("S must be non-empty")
    if len(denominators) != len(set(denominators)):
        raise ValueError("S must not contain duplicate denominators")

    max_v = max(valuation(denominator, q) for denominator in denominators)
    top = tuple(denominator for denominator in denominators if valuation(denominator, q) == max_v)
    residue = 0
    for denominator in top:
        reduced = denominator
        for _ in range(max_v):
            reduced //= q
        residue = (residue + pow(reduced % q, -1, q)) % q

    return TopLayerResidue(
        prime=q,
        max_valuation=max_v,
        top_denominators=top,
        residue_sum_mod_q=residue,
    )


def run_examples() -> None:
    examples = [
        ((8, 24), 2, TopLayerResidue(2, 3, (8, 24), 0)),
        ((12, 20), 2, TopLayerResidue(2, 2, (12, 20), 0)),
        ((18, 20, 22), 19, TopLayerResidue(19, 0, (18, 20, 22), 13)),
        ((18, 20, 22), 37, TopLayerResidue(37, 0, (18, 20, 22), 6)),
    ]
    errors: list[str] = []
    for S, q, expected in examples:
        actual = top_layer_residue_sum(S, q)
        print(
            f"S={S} q={q}: max_v={actual.max_valuation} "
            f"top={actual.top_denominators} residue={actual.residue_sum_mod_q}"
        )
        if actual != expected:
            errors.append(f"S={S} q={q}: expected {expected}, found {actual}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"  {error}")
        raise SystemExit(1)
    print("PASS")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute q-adic top-layer residue sums.")
    parser.add_argument("--q", type=int)
    parser.add_argument("--S", nargs="*", type=int)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test or args.q is None:
        run_examples()
        return
    if not args.S:
        raise SystemExit("--S is required when --q is provided")

    result = top_layer_residue_sum(args.S, args.q)
    print(f"q: {result.prime}")
    print(f"max_valuation: {result.max_valuation}")
    print(f"top_denominators: {','.join(str(value) for value in result.top_denominators)}")
    print(f"residue_sum_mod_q: {result.residue_sum_mod_q}")


if __name__ == "__main__":
    main()
