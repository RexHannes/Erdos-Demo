# MathOverflow Draft: A finite p-adic saturation pattern in an Erdős #287 computation

I am looking for conceptual explanations for a finite pattern that appeared in a computational experiment related to Erdős #287. I am not claiming a proof of the problem.

For finite searches with denominator cutoffs `N = 65` and `N = 70`, I enumerated candidate denominator sets `S` in a near-sum window around 1 and recorded which prime-modulus top-layer obstructions eliminate each candidate. The candidate-level datasets packaged here use the wide window `[0.99, 1.01]`.

Two prime-pair backbones are especially close to covering all candidates:

```text
{2,31}: 68 exceptions
{19,37}: 69 exceptions
```

The striking finite observation is that the N65 and N70 exported anomaly row sets are identical after normalizing by denominator set:

```text
N65 rows:          137
N70 rows:          137
N65 not in N70:      0
N70 not in N65:      0
max denominator:    36
```

A small sentinel check gives the expected cutoff behavior:

```text
N35 rows: 116
N36 rows: 137
N70 rows: 137
N36 vs N70 difference count: 0
```

The rows also have forced small cores:

```text
Every computed 2+31 exception contains {15,17}.
Every computed 19+37 exception contains {18,20}.
```

For the N65 labels, the 137 rows have the following finite template split:

```text
2+31 + {8,24}:      63
2+31 + {12,20}:      5
19+37 + {22}:       58
19+37 + {21,23}:    11
unclassified:        0
```

The question is not whether this finite computation proves Erdős #287. It does not. The question is:

> Is there a known p-adic or Egyptian-fraction mechanism that would naturally explain denominator localization at `36` and forced cores such as `{15,17}` and `{18,20}` in the exceptions to these near-covering prime pairs?

The repository contains:

```text
erdosdemo/data/anomalies_N65_candidates.csv
erdosdemo/data/anomalies_N70_candidates.csv
erdosdemo/scripts/verify_n65_n70_audit.py
erdosdemo/scripts/verify_residue_blocks.py
erdosdemo/notes/top_layer_obstruction.md
erdosdemo/notes/n65_finite_pattern.md
```

The intended minimal verification command is:

```bash
python3 erdosdemo/scripts/verify_n65_n70_audit.py
```

I would especially appreciate pointers to comparable finite p-adic obstruction phenomena, or reasons this kind of denominator localization and small-core split should be expected rather than exceptional.
