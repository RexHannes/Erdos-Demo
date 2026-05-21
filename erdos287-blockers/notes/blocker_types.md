# Blocker Types

This file is a registry template for blocker mechanisms related to Erdős Problem #287.

Status labels:

- `proved`: trigger, obstruction prime, forced denominators, gap forcing, maximal p-adic layer, residue contradiction, and valid range are explicit.
- `candidate`: the shape looks plausible, but at least one proof field is not yet explicit.
- `observed`: the pattern appears in data only.

Do not use this registry to claim a proof of Erdős #287.

## Template

```text
name:
status: proved / candidate / observed
trigger number near M:
obstruction prime q:
forced denominators:
why gap<=2 forces them:
maximal q-adic layer:
residue contradiction:
valid M-range:
notes:
```

## Woett W_minus

```text
name: Woett W_minus
status: proved for the baseline interval lemma
trigger number near M: prime p with r = (p-1)/2 prime
obstruction prime q: q = p if the forced denominator is p; q = r if the forced denominator is 2r = p-1
forced denominators: one of p or 2r = p-1
why gap<=2 forces them:
  If p lies in (M/2+1, M), equivalently M in [p+1, 2p-3], then the gap<=2 chain from below M/2 to M cannot jump over the local block around p. Since p and p-1=2r are the available prime / twice-prime triggers in this Woett-good case, one of these triggers supplies the obstruction.
maximal q-adic layer:
  The forced prime or twice-prime denominator contributes a top-layer term for its large prime divisor.
residue contradiction:
  The top layer contains a single nonzero reciprocal residue modulo the obstruction prime, so the reciprocal sum cannot be an integer.
valid M-range: M in [p+1, 2p-3]
notes:
  This entry records the Woett-good-prime interval baseline. Generalized blockers must not be marked proved merely by analogy.
```

## Woett W_plus

```text
name: Woett W_plus
status: proved for the baseline interval lemma
trigger number near M: prime p with r = (p+1)/2 prime
obstruction prime q: q = p if the forced denominator is p; q = r if the forced denominator is 2r = p+1
forced denominators: one of p or 2r = p+1
why gap<=2 forces them:
  If p lies in (M/2+1, M), equivalently M in [p+1, 2p-3], then the gap<=2 chain from below M/2 to M cannot jump over the local block around p. Since p and p+1=2r are the available prime / twice-prime triggers in this Woett-good case, one of these triggers supplies the obstruction.
maximal q-adic layer:
  The forced prime or twice-prime denominator contributes a top-layer term for its large prime divisor.
residue contradiction:
  The top layer contains a single nonzero reciprocal residue modulo the obstruction prime, so the reciprocal sum cannot be an integer.
valid M-range: M in [p+1, 2p-3]
notes:
  This entry records the Woett-good-prime interval baseline. Generalized blockers must not be marked proved merely by analogy.
```

## Thirteen Old Cover Types

The older cover types should be entered here only as candidate or observed records until their trigger and obstruction roles are separated.

```text
name: old-cover-type-01
status: observed
trigger number near M: TODO
obstruction prime q: TODO
forced denominators: TODO
why gap<=2 forces them: TODO
maximal q-adic layer: TODO
residue contradiction: TODO
valid M-range: TODO
notes: imported from old cover taxonomy only after proof fields are separated.
```

```text
name: old-cover-type-02
status: observed
trigger number near M: TODO
obstruction prime q: TODO
forced denominators: TODO
why gap<=2 forces them: TODO
maximal q-adic layer: TODO
residue contradiction: TODO
valid M-range: TODO
notes: imported from old cover taxonomy only after proof fields are separated.
```

Repeat the same template for old-cover-type-03 through old-cover-type-13 as evidence becomes available.
