# Top-Layer Obstruction Lemma

Let `p` be prime and let `S` be a finite set of positive denominators. Write each denominator as

```text
n = p^v u
```

with `p` not dividing `u`. Let

```text
V = max_{n in S} v_p(n).
```

After multiplying the reciprocal sum by `p^V`, all terms with valuation below `V` become divisible by `p`. Modulo `p`, only the top-layer terms with `v_p(n) = V` remain:

```text
p^V sum_{n in S} 1/n
  == sum_{v_p(n)=V} u_n^{-1} mod p.
```

Therefore, if

```text
sum_{v_p(n)=V} u_n^{-1} != 0 mod p,
```

then the reciprocal sum cannot be an integer. In the computational language used here, prime `p` kills that candidate.

This is only a finite obstruction test. It is not a proof of Erdős #287, and it does not by itself classify all possible denominator structures.

For the N=65 finite dataset, the small blocks

```text
{8,24}
{12,20}
```

are examples of top-2-adic cancellation: both top-layer residues sum to `0 mod 2`.

The notes deliberately avoid claiming that any denominator such as `16` is universally absent. The verified finite statement in this demo is the four-template classification of the supplied CSV, not a general structural theorem.

