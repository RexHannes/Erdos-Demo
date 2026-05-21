# Erdős 287 Blocker Baseline

This module is a reproducible computational baseline for the Woett / robertboy18 blocker route for Erdős Problem #287. It is not a proof of Erdős #287.

The goal is deliberately narrow:

- verify a chain of Woett-good primes;
- build the coverage intervals supplied by that chain;
- output the uncovered `M` values, called holes;
- provide small reusable p-adic top-layer utilities for later blocker experiments.

## Woett-Good Primes

A prime `p` is called Woett-good here if either

```text
(p-1)/2
```

or

```text
(p+1)/2
```

is prime.

Such a prime covers maximum-denominator values

```text
M in [p+1, 2p-3].
```

Equivalently, `p` lies in the interval `(M/2+1, M)`. A chain is continuous when consecutive primes satisfy

```text
p_next <= 2*p - 3.
```

The key output is the holes table: uncovered values of `M` up to a requested bound `N`.

## Files

- `data/woett_chain.txt`: one integer `p` per line; blank lines and `#` comments are ignored.
- `scripts/verify_woett_chain.py`: verifies primality, Woett-goodness, and chain continuity.
- `scripts/scan_woett_holes.py`: builds intervals and outputs uncovered `M <= N`.
- `scripts/padic_top_layer.py`: reusable p-adic top-layer residue helper.
- `notes/blocker_types.md`: registry template for proved/candidate/observed blocker mechanisms.
- `results/`: generated sample outputs from the tiny placeholder chain.

## Commands

From the repository root:

```bash
python3 erdos287-blockers/scripts/verify_woett_chain.py
python3 erdos287-blockers/scripts/scan_woett_holes.py --N 120
python3 erdos287-blockers/scripts/padic_top_layer.py --self-test
```

Expected sample output:

```text
chain: erdos287-blockers/data/woett_chain.txt
primes: 7
errors: 0
PASS
```

```text
N: 120
holes: 10
holes_preview: 1,2,3,4,5,116,117,118,119,120
PASS
```

```text
S=(8, 24) q=2: max_v=3 top=(8, 24) residue=0
S=(12, 20) q=2: max_v=2 top=(12, 20) residue=0
S=(18, 20, 22) q=19: max_v=0 top=(18, 20, 22) residue=13
S=(18, 20, 22) q=37: max_v=0 top=(18, 20, 22) residue=6
PASS
```

## GitHub Artifacts

The workflow `.github/workflows/erdos287-blockers.yml` runs the three commands above and uploads `erdos287-blockers/results/` as a GitHub Actions artifact named `erdos287-blockers-results`.

## Scope Notes

The sample chain is only a tiny placeholder. Paste the full forum chain into `data/woett_chain.txt` before treating the holes table as meaningful evidence.

The blocker registry keeps `proved`, `candidate`, and `observed` labels separate. Do not mark generalized blockers as proved until the trigger, obstruction prime, forced denominators, and p-adic contradiction are all explicit.
